
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import json
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut



import WebMirror.OutputFilters.rss.ParserFuncs as pfuncs

from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import WebMirror.OutputFilters.FilterBase
import WebMirror.rules
import flags

skip_filter = [
	"www.baka-tsuki.org",
	"re-monster.wikia.com",
	'inmydaydreams.com',
	'www.fanfiction.net',
	'www.booksie.com',
	'www.booksiesilk.com',
	'www.fictionpress.com',
	'storiesonline.net',
	'www.fictionmania.tv',

]



class DataParser(WebMirror.OutputFilters.FilterBase.FilterBase):

	amqpint = None
	amqp_connect = True

	def __init__(self, transfer=True, debug_print=False, write_debug=False, **kwargs):
		super().__init__(**kwargs)

		self.dbg_print = debug_print
		self.transfer = transfer
		self.names = set()

		self.write_debug = write_debug

	####################################################################################################################################################
	####################################################################################################################################################
	##
	##  Dispatcher
	##
	####################################################################################################################################################
	####################################################################################################################################################


	def dispatchRelease(self, item):

		ret = False

		funcMap = {

				"'Ball'-Kicking Gang Boss"                                      : pfuncs.extractBallKickingGangBoss,
				"Cautr's"                                                       : pfuncs.extractCautrs,
				"DOW's Translations"                                            : pfuncs.extractDOWsTranslations,
				"Dreamless Window's translation"                                : pfuncs.extractDreamlessWindowsTranslation,
				"Evida's Indo Romance"                                          : pfuncs.extractEvidasIndoRomance,
				"Hon'yaku"                                                      : pfuncs.extractHonyaku,
				"Monkoto's Translations"                                        : pfuncs.extractMonkotosTranslations,
				"Pandora's Book"                                                : pfuncs.extractPandorasBook,
				"Rui's Translations"                                            : pfuncs.extractRuisTranslations,
				"WizThief's Novels"                                             : pfuncs.extractWizThiefsNovels,
				"Xiaowen206's Blog"                                             : pfuncs.extractXiaowen206sBlog,
				"Zxzxzx's blog"                                                 : pfuncs.extractZxzxzxsBlog,
				'(NanoDesu) - Amagi Brilliant Park '                            : pfuncs.extractNanoDesuAmagiBrilliantPark,
				'(NanoDesu) - Fate/Apocrypha'                                   : pfuncs.extractNanoDesuFateApocrypha,
				'(NanoDesu) - Fuyuu Gakuen no Alice and Shirley'                : pfuncs.extractNanoDesuFuyuuGakuennoAliceandShirley,
				'(NanoDesu) - Gekka no Utahime to Magi no Ou'                   : pfuncs.extractNanoDesuGekkanoUtahimetoMaginoOu,
				'(NanoDesu) - GJ-Bu'                                            : pfuncs.extractNanoDesuGJBu,
				'(NanoDesu) - Hai to Gensou no Grimgal'                         : pfuncs.extractNanoDesuHaitoGensounoGrimgal,
				'(NanoDesu) - Hentai Ouji to Warawanai Neko'                    : pfuncs.extractNanoDesuHentaiOujitoWarawanaiNeko,
				'(NanoDesu) - Kono Sekai ga Game Dato Ore Dake ga Shitteiru'    : pfuncs.extractNanoDesuKonoSekaigaGameDatoOreDakegaShitteiru,
				'(NanoDesu) - Kore wa Zombie Desu ka?'                          : pfuncs.extractNanoDesuKorewaZombieDesuka,
				'(NanoDesu) - Kurenai'                                          : pfuncs.extractNanoDesuKurenai,
				'(NanoDesu) - Love★You'                                         : pfuncs.extractNanoDesuLoveYou,
				'(NanoDesu) - Maoyuu Maou Yuusha'                               : pfuncs.extractNanoDesuMaoyuuMaouYuusha,
				'(NanoDesu) - Mayo Chiki'                                       : pfuncs.extractNanoDesuMayoChiki,
				'(NanoDesu) - Ojamajo Doremi'                                   : pfuncs.extractNanoDesuOjamajoDoremi,
				'(NanoDesu) - Oreimo'                                           : pfuncs.extractNanoDesuOreimo,
				'(NanoDesu) - Rokka no Yuusha'                                  : pfuncs.extractNanoDesuRokkanoYuusha,
				'(NanoDesu) - Saenai Heroine no Sodatekata'                     : pfuncs.extractNanoDesuSaenaiHeroinenoSodatekata,
				'(NanoDesu) - Sasami-San@Ganbaranai'                            : pfuncs.extractNanoDesuSasamiSanGanbaranai,
				'(NanoDesu) - Seitokai no Ichizon'                              : pfuncs.extractNanoDesuSeitokainoIchizon,
				'(NanoDesu) - Sky World'                                        : pfuncs.extractNanoDesuSkyWorld,
				'(NanoDesu) - Yahari Ore no Seishun Love Come wa Machigatteiru' : pfuncs.extractNanoDesuYahariOrenoSeishunLoveComewaMachigatteiru,
				'-Sloth-'                                                       : pfuncs.extractSloth,
				'/'                                                             : pfuncs.extractForwardSlash,
				'12 Superlatives'                                               : pfuncs.extract12Superlatives,
				'1HP'                                                           : pfuncs.extract1HP,
				'77 Novel'                                                      : pfuncs.extract77Novel,
				'87 Percent Translation'                                        : pfuncs.extract87Percent,
				'[G.O] Chronicles'                                              : pfuncs.extractGOChronicles,
				'[nakulas]'                                                     : pfuncs.extractNakulas,
				'A fish once said this to me'                                   : pfuncs.extractDarkFish,
				'A Grey World'                                                  : pfuncs.extractAGreyWorld,
				'A Pearly View'                                                 : pfuncs.extractAPearlyView,
				'A Place Of Legends'                                            : pfuncs.extractPlaceOfLegends,
				'A Translator\'s Ramblings'                                     : pfuncs.extractATranslatorsRamblings,
				'A traveler\'s translations.'                                   : pfuncs.extractATravelersTranslations,
				'A0132'                                                         : pfuncs.extractA0132,
				'Adamantine Dragon in the Crystal World'                        : pfuncs.extractAdamantineDragonintheCrystalWorld,
				'AFlappyTeddyBird'                                              : pfuncs.extractAFlappyTeddyBird,
				'Alcsel Translations'                                           : pfuncs.extractAlcsel,
				'Alice Translations'                                            : pfuncs.extractAliceTranslations,
				'alicetranslations.wordpress.com'                               : pfuncs.extractAlicetranslations,
				'All\'s Fair In Love & War'                                     : pfuncs.extractAllsFairInLoveWar,
				'Altoroc Translations'                                          : pfuncs.extractAltorocTranslations,
				'Alyschu & Co'                                                  : pfuncs.extractAlyschuCo,
				'Amery Edge'                                                    : pfuncs.extractAmeryEdge,
				'Anathema Serial'                                               : pfuncs.extractAnathema,
				'Andrew9495\'s MTL corner'                                      : pfuncs.extractAndrew9495,
				'Anne And Cindy'                                                : pfuncs.extractAnneAndCindy,
				'Anon Empire'                                                   : pfuncs.extractAnonEmpire,
				'Another Parallel World'                                        : pfuncs.extractAnotherParallelWorld,
				'Another World Translations'                                    : pfuncs.extractAnotherWorldTranslations,
				'Aori Translations'                                             : pfuncs.extractAoriTranslations,
				'Aqua Scans'                                                    : pfuncs.extractAquaScans,
				'Aquarilas\' Scenario'                                          : pfuncs.extractAquarilasScenario,
				'Aran Translations'                                             : pfuncs.extractAranTranslations,
				'Archivity'                                                     : pfuncs.extractArchivity,
				'Ares Novels'                                                   : pfuncs.extractAresNovels,
				'Ark Machine Translations'                                      : pfuncs.extractArkMachineTranslations,
				'asd398'                                                        : pfuncs.extractAsd398,
				'AsherahBlue\'s Notebook'                                       : pfuncs.extractAsherahBlue,
				'Aten Translations'                                             : pfuncs.extractAtenTranslations,
				'Avert Translations'                                            : pfuncs.extractAvert,
				'Ayax World'                                                    : pfuncs.extractAyaxWorld,
				'Azure Sky Translation'                                         : pfuncs.extractAzureSky,
				'Azurro 4 Cielo'                                                : pfuncs.extractAzurro,
				'Bad Translation'                                               : pfuncs.extractBadTranslation,
				'Baka Dogeza Translation'                                       : pfuncs.extractBakaDogeza,
				'Baka Pervert'                                                  : pfuncs.extractBakaPervert,
				'Bayabusco Translation'                                         : pfuncs.extractBayabuscoTranslation,
				'Bcat00 Translation'                                            : pfuncs.extractBcat00,
				'Bear Bear Translations'                                        : pfuncs.extractBearBearTranslations,
				'Beehugger'                                                     : pfuncs.extractBeehugger,
				'Berseker Translations'                                         : pfuncs.extractBersekerTranslations,
				'BeRsErk Translations'                                          : pfuncs.extractBeRsErkTranslations,
				'Bijinsans'                                                     : pfuncs.extractBijinsans,
				'Binggo&Corp'                                                   : pfuncs.extractBinggoCorp,
				'Binhjamin'                                                     : pfuncs.extractBinhjamin,
				'Blade of Hearts'                                               : pfuncs.extractBladeOfHearts,
				'Blublub'                                                       : pfuncs.extractBlublub,
				'Blue Silver Translations'                                      : pfuncs.extractBlueSilverTranslations,
				'Bluefire Translations'                                         : pfuncs.extractBluefireTranslations,
				'Books Movies and Beyond'                                       : pfuncs.extractBooksMoviesAndBeyond,
				'Bruin Translation'                                             : pfuncs.extractBruinTranslation,
				'Bu Bu Jing Xin Translation'                                    : pfuncs.extractBuBuJingXinTrans,
				'Burei Dan Works'                                               : pfuncs.extractBureiDan,
				'C Novels 2 C'                                                  : pfuncs.extractCNovels2C,
				'C-Novel Tranlations…'                                          : pfuncs.extractCNovelTranlations,
				'C.E. Light Novel Translations'                                 : pfuncs.extractCeLn,
				'Calico x Tabby'                                                : pfuncs.extractCalicoxTabby,
				'Cas Project Site'                                              : pfuncs.extractCasProjectSite,
				'Cat Scans'                                                     : pfuncs.extractCatScans,
				'CaveScans'                                                     : pfuncs.extractCaveScans,
				'cavescans.com'                                                 : pfuncs.extractCavescans,
				'Ceruleonice Translations'                                      : pfuncs.extractCeruleonice,
				'Cheddar!'                                                      : pfuncs.extractCheddar,
				'Chinese BL Translations'                                       : pfuncs.extractChineseBLTranslations,
				'Chinese Weaboo Translations'                                   : pfuncs.extractChineseWeabooTranslations,
				'Chrona Zero'                                                   : pfuncs.extractChronaZero,
				'Chronon Translations'                                          : pfuncs.extractChrononTranslations,
				'ChubbyCheeks'                                                  : pfuncs.extractChubbyCheeks,
				'Circle of Shards'                                              : pfuncs.extractCircleofShards,
				'Circus Translations'                                           : pfuncs.extractCircusTranslations,
				'Clicky Click Translation'                                      : pfuncs.extractClicky,
				'Cloud Manor'                                                   : pfuncs.extractCloudManor,
				'Cloud Translations'                                            : pfuncs.extractCloudTranslations,
				'Clover\'s Nook'                                                : pfuncs.extractCloversNook,
				'Code-Zero\'s Blog'                                             : pfuncs.extractCodeZerosBlog,
				'CookiePasta Translations'                                      : pfuncs.extractCookiePastaTranslations,
				'CookiePasta'                                                   : pfuncs.extractCookiePasta,
				'Cosmic Translation'                                            : pfuncs.extractCosmicTranslation,
				'Crappy Machine Translation'                                    : pfuncs.extractCrappyMachineTranslation,
				'Crazy for HE Novels'                                           : pfuncs.extractCrazyForHENovels,
				'CrystalRainDescends'                                           : pfuncs.extractCrystalRainDescends,
				'CtrlAlcalá'                                                    : pfuncs.extractCtrlAlcala,
				'Currently TLing [Bu ni Mi]'                                    : pfuncs.extractCurrentlyTLingBuniMi,
				'DadIsHero Fan Translations'                                    : pfuncs.extractDadIsHeroFanTranslations,
				'Daily-Dallying'                                                : pfuncs.extractDailyDallying,
				'Dao Seeker Blog'                                               : pfuncs.extractDaoSeekerBlog,
				'Dark Translations'                                             : pfuncs.extractDarkTranslations,
				'Dawning Howls'                                                 : pfuncs.extractDawningHowls,
				'Deadly Forgotten Legends'                                      : pfuncs.extractDeadlyForgottenLegends,
				'Defan\'s Translations'                                         : pfuncs.extractDefansTranslations,
				'Defiring'                                                      : pfuncs.extractDefiring,
				'Dekinai Diary'                                                 : pfuncs.extractDekinaiDiary,
				'Delicious Translations'                                        : pfuncs.extractDeliciousTranslations,
				'Demerith Translation'                                          : pfuncs.extractDemerithTranslation,
				'Descent Subs'                                                  : pfuncs.extractDescentSubs,
				'Dewey Night Unrolls'                                           : pfuncs.extractDeweyNightUnrolls,
				'DHH Translations'                                              : pfuncs.extractDHHTranslations,
				'Disappointing Translations'                                    : pfuncs.extractDisappointingTranslations,
				'Distracted Chinese'                                            : pfuncs.extractDistractedChinese,
				'Distracted Translations'                                       : pfuncs.extractDistractedTranslations,
				'Diwasteman'                                                    : pfuncs.extractDiwasteman,
				'Dorayakiz'                                                     : pfuncs.extractDorayakiz,
				'DragomirCM'                                                    : pfuncs.extractDragomirCM,
				'Dragon MT'                                                     : pfuncs.extractDragonMT,
				'Dreadful Decoding'                                             : pfuncs.extractDreadfulDecoding,
				'Dream Avenue'                                                  : pfuncs.extractDreamAvenue,
				'Dreams of Jianghu'                                             : pfuncs.extractDreamsOfJianghu,
				'Ducky\'s English Translations'                                 : pfuncs.extractDuckysEnglishTranslations,
				'Duran Daru Translation'                                        : pfuncs.extractDuranDaruTranslation,
				'Durasama'                                                      : pfuncs.extractDurasama,
				'Dynamis Gaul Light Novel'                                      : pfuncs.extractDynamisGaul,
				'EC Webnovel'                                                   : pfuncs.extractECWebnovel,
				'EccentricTranslations'                                         : pfuncs.extractEccentricTranslations,
				'ELYSION Translation'                                           : pfuncs.extractELYSIONTranslation,
				'Emergency Exit\'s Release Blog'                                : pfuncs.extractEmergencyExitsReleaseBlog,
				'Emruyshit Translations'                                        : pfuncs.extractEmruyshitTranslations,
				'End Online Novel'                                              : pfuncs.extractEndOnline,
				'EndKun'                                                        : pfuncs.extractEndKun,
				'Ensj Translations'                                             : pfuncs.extractEnsjTranslations,
				'Ente38 translations'                                           : pfuncs.extractEnte38translations,
				'EnTruce Translations'                                          : pfuncs.extractEnTruceTranslations,
				'Epithetic'                                                     : pfuncs.extractEpithetic,
				'Epyon Translations'                                            : pfuncs.extractEpyonTranslations,
				'Ero Light Novel Translations'                                  : pfuncs.extractEroLightNovelTranslations,
				'Eros Workshop'                                                 : pfuncs.extractErosWorkshop,
				'eternalpath.net'                                               : pfuncs.extractEternalpath,
				'Etheria Translations'                                          : pfuncs.extractEtheriaTranslations,
				'Eugene Rain'                                                   : pfuncs.extractEugeneRain,
				'Eye of Adventure '                                             : pfuncs.extractEyeofAdventure,
				'EZ Translations'                                               : pfuncs.extractEZTranslations,
				'Fak Translations'                                              : pfuncs.extractFakTranslations,
				'Fake typist'                                                   : pfuncs.extractFaketypist,
				'Falamar Translation'                                           : pfuncs.extractFalamarTranslation,
				'Falinmer'                                                      : pfuncs.extractFalinmer,
				'Fanatical'                                                     : pfuncs.extractFanatical,
				'FeedProxy'                                                     : pfuncs.extractFeedProxy,
				'fgiLaN translations'                                           : pfuncs.extractfgiLaNTranslations,
				'Fighting Dreamers Scanlations'                                 : pfuncs.extractFightingDreamersScanlations,
				'Firebird\'s Nest'                                              : pfuncs.extractFirebirdsNest,
				'Five Star Specialists'                                         : pfuncs.extractFiveStar,
				'Flicker Hero'                                                  : pfuncs.extractFlickerHero,
				'Flower Bridge Too'                                             : pfuncs.extractFlowerBridgeToo,
				'Forgetful Dreamer'                                             : pfuncs.extractForgetfulDreamer,
				'Forgotten Conqueror'                                           : pfuncs.extractForgottenConqueror,
				'Frostfire 10'                                                  : pfuncs.extractFrostfire10,
				'Fudge Translations'                                            : pfuncs.extractFudgeTranslations,
				'Fung Shen'                                                     : pfuncs.extractFungShen,
				'Fuzion Life'                                                   : pfuncs.extractFuzionLife,
				'Gaochao Translations'                                          : pfuncs.extractGaochaoTranslations,
				'Gargoyle Web Serial'                                           : pfuncs.extractGargoyleWebSerial,
				'Gila Translation Monster'                                      : pfuncs.extractGilaTranslation,
				'Giraffe Corps'                                                 : pfuncs.extractGiraffe,
				'Goddess! Grant Me a Girlfriend!!'                              : pfuncs.extractGoddessGrantMeaGirlfriend,
				'Gravity Tales'                                                 : pfuncs.extractGravityTranslation,
				'GrimdarkZ Translations'                                        : pfuncs.extractGrimdarkZTranslations,
				'Grow with Me'                                                  : pfuncs.extractGrowWithMe,
				'Grow with me'                                                  : pfuncs.extractGrowWithMe,
				'guhehe.TRANSLATIONS'                                           : pfuncs.extractGuhehe,
				'Guro Translation'                                              : pfuncs.extractGuroTranslation,
				'Hajiko translation'                                            : pfuncs.extractHajiko,
				'Hamster428'                                                    : pfuncs.extractHamster428,
				'HaruPARTY'                                                     : pfuncs.extractHaruPARTY,
				'Heart Crusade Scans'                                           : pfuncs.extractHeartCrusadeScans,
				'Helidwarf'                                                     : pfuncs.extractHelidwarf,
				'Hell Yeah 524'                                                 : pfuncs.extractHellYeah524,
				'Hello Translations'                                            : pfuncs.extractHelloTranslations,
				'Hellping'                                                      : pfuncs.extractHellping,
				'Hendricksen-sama'                                              : pfuncs.extractHendricksensama,
				'Henouji Translation'                                           : pfuncs.extractHenoujiTranslation,
				'Heroic Legend of Arslan Translations'                          : pfuncs.extractHeroicLegendOfArslanTranslations,
				'Heroic Novels'                                                 : pfuncs.extractHeroicNovels,
				'Hikki no Mori Translations'                                    : pfuncs.extractHikkinoMoriTranslations,
				'Hokage Translations'                                           : pfuncs.extractHokageTrans,
				'Hold \'X\' and Click'                                          : pfuncs.extractHoldX,
				'Hot Cocoa Translations'                                        : pfuncs.extractHotCocoa,
				'Hyorinmaru Blog'                                               : pfuncs.extractHyorinmaruBlog,
				'Hyorinmaru'                                                    : pfuncs.extractHyorinmaruBlog,
				'Imoutolicious Light Novel Translations'                        : pfuncs.extractImoutolicious,
				'Infinite Novel Translations'                                   : pfuncs.extractInfiniteNovelTranslations,
				'Infinite Translations'                                         : pfuncs.extractInfiniteTranslations,
				'IntenseDesSugar'                                               : pfuncs.extractIntenseDesSugar,
				'Isekai Mahou Translations!'                                    : pfuncs.extractIsekaiMahou,
				'Isekai Soul-Cyborg Translations'                               : pfuncs.extractIsekaiTranslation,
				'Isolarium'                                                     : pfuncs.extractIsolarium,
				'Istian\'s Workshop'                                            : pfuncs.extractIstiansWorkshop,
				'Iterations within a Thought-Eclipse'                           : pfuncs.extractIterations,
				'itranslateln'                                                  : pfuncs.extractItranslateln,
				'izra709 | B Group no Shounen Translations'                     : pfuncs.extractIzra709,
				'Jagaimo'                                                       : pfuncs.extractJagaimo,
				'Januke Translations'                                           : pfuncs.extractJanukeTranslations,
				'Japtem'                                                        : pfuncs.extractJaptem,
				'JawzTranslations'                                              : pfuncs.extractJawzTranslations,
				'Joeglen\'s Translation Space'                                  : pfuncs.extractJoeglensTranslationSpace,
				'Joie de Vivre'                                                 : pfuncs.extractJoiedeVivre,
				'Jun Juntianxia'                                                : pfuncs.extractJunJuntianxia,
				'Kaezar Translations'                                           : pfuncs.extractKaezar,
				'Kahoim Translations'                                           : pfuncs.extractKahoim,
				'Kakkokari'                                                     : pfuncs.extractKakkokari,
				'Kami Translation'                                              : pfuncs.extractKamiTranslation,
				'Kawaii Daikon'                                                 : pfuncs.extractKawaiiDaikon,
				'Kedelu'                                                        : pfuncs.extractKedelu,
				'Kerambit\'s Incisions'                                         : pfuncs.extractKerambit,
				'Keyo Translations'                                             : pfuncs.extractKeyoTranslations,
				'King Jaahn\'s Subjects'                                        : pfuncs.extractKingJaahn,
				'Kiri Leaves'                                                   : pfuncs.extractKiri,
				'Kisato\'s MLTs'                                                : pfuncs.extractKisatosMLTs,
				'KN Translation'                                                : pfuncs.extractKNTranslation,
				'Knokkro Translations'                                          : pfuncs.extractKnokkroTranslations,
				'KobatoChanDaiSukiScan'                                         : pfuncs.extractKobatoChanDaiSukiScan,
				'Kokuma Translations'                                           : pfuncs.extractKokumaTranslations,
				'Konobuta'                                                      : pfuncs.extractKonobuta,
				'Koong Koong Translations'                                      : pfuncs.extractKoongKoongTranslations,
				'Kore Yori Hachidori'                                           : pfuncs.extractKoreYoriHachidori,
				'Korean Novel Translations'                                     : pfuncs.extractKoreanNovelTrans,
				'Krytyk\'s Translations'                                        : pfuncs.extractKrytyksTranslations,
				'Kuma Otou'                                                     : pfuncs.extractKumaOtou,
				'Kuro Translations'                                             : pfuncs.extractKuroTranslations,
				'Kurotsuki Novel'                                               : pfuncs.extractKurotsukiNovel,
				'Kyakka Translations'                                           : pfuncs.extractKyakkaTranslations,
				'Kyakka'                                                        : pfuncs.extractKyakka,
				'kyoptionslibrary.blogspot.com'                                 : pfuncs.extractKyoptionslibrary,
				'L2M'                                                           : pfuncs.extractL2M,
				'Larvyde'                                                       : pfuncs.extractLarvyde,
				'Lascivious Imouto'                                             : pfuncs.extractLasciviousImouto,
				'Lastvoice Translator'                                          : pfuncs.extractLastvoiceTranslator,
				'Layzisheep'                                                    : pfuncs.extractLayzisheep,
				'Lazy NEET Translations'                                        : pfuncs.extractNEET,
				'Legend of Galactic Heroes Translation Project'                 : pfuncs.extractLegendofGalacticHeroes,
				'Lickymee Translations'                                         : pfuncs.extractLickymeeTranslations,
				'Light Novel translations'                                      : pfuncs.extractLightNoveltranslations,
				'Light Novels Translations'                                     : pfuncs.extractLightNovelsTranslations,
				'Lil\' Bliss Novels'                                            : pfuncs.extractLilBlissNovels,
				'Ling Translates Sometimes'                                     : pfuncs.extractLingTranslatesSometimes,
				'Lingson\'s Translations'                                       : pfuncs.extractLingson,
				'Linked Translations'                                           : pfuncs.extractLinkedTranslations,
				'Little Novel Translation'                                      : pfuncs.extractLittleNovelTranslation,
				'Little Translations'                                           : pfuncs.extractLittleTranslations,
				'LittleShanks Translations'                                     : pfuncs.extractLittleShanksTranslations,
				'Lizard Translations'                                           : pfuncs.extractLizardTranslations,
				'LMS Machine Translations'                                      : pfuncs.extractLMSMachineTranslations,
				'Ln Addiction'                                                  : pfuncs.extractLnAddiction,
				'Lohithbb TLs'                                                  : pfuncs.extractLohithbbTLs,
				'Loiterous'                                                     : pfuncs.extractLoiterous,
				'Lonahora'                                                      : pfuncs.extractLonahora,
				'LorCromwell'                                                   : pfuncs.extractLorCromwell,
				'LordofScrubs'                                                  : pfuncs.extractLordofScrubs,
				'Lost in Translation'                                           : pfuncs.extractLostInTranslation,
				'Luen Translations'                                             : pfuncs.extractLuenTranslations,
				'Lunaris'                                                       : pfuncs.extractLunaris,
				'Lunate'                                                        : pfuncs.extractLunate,
				'LygarTranslations'                                             : pfuncs.extractLygarTranslations,
				'Lylis Translations'                                            : pfuncs.extractLylisTranslations,
				'Lynfamily'                                                     : pfuncs.extractLynfamily,
				'Lypheon Machine Translation'                                   : pfuncs.extractLypheonMachineTranslation,
				'Machine Sliced Bread'                                          : pfuncs.extractMachineSlicedBread,
				'Madao Translations'                                            : pfuncs.extractMadaoTranslations,
				'MadoSpicy TL'                                                  : pfuncs.extractMadoSpicy,
				'Mahou Koukoku'                                                 : pfuncs.extractMahouKoukoku,
				'Mahoutsuki Translation'                                        : pfuncs.extractMahoutsuki,
				'Makina Translations'                                           : pfuncs.extractMakinaTranslations,
				'Mana Tank Magus'                                               : pfuncs.extractManaTankMagus,
				'Manga0205 Translations'                                        : pfuncs.extractManga0205Translations,
				'Maou na Anoko to murabito a'                                   : pfuncs.extractMaounaAnokotomurabitoa,
				'Martial God Translator'                                        : pfuncs.extractMartialGodTranslator,
				'Mecha Mushroom Translations'                                   : pfuncs.extractMechaMushroom,
				'Midnight Translation Blog'                                     : pfuncs.extractMidnightTranslationBlog,
				'Mike777ac'                                                     : pfuncs.extractMike777ac,
				'Mnemeaa'                                                       : pfuncs.extractMnemeaa,
				'Mojo Translations'                                             : pfuncs.extractMojoTranslations,
				'Monk Translation'                                              : pfuncs.extractMonkTranslation,
				'Moon Bunny Cafe'                                               : pfuncs.extractMoonBunnyCafe,
				'Morrighan Sucks'                                               : pfuncs.extractMorrighanSucks,
				'Mousou Haven'                                                  : pfuncs.extractMousouHaven,
				'mousou-haven.com'                                              : pfuncs.extractMousouhaven,
				'MTLCrap'                                                       : pfuncs.extractMTLCrap,
				'My Purple World'                                               : pfuncs.extractMyPurpleWorld,
				'Mystique Translations'                                         : pfuncs.extractMystiqueTranslations,
				'Mythical Pagoda'                                               : pfuncs.extractMythicalPagoda,
				'N00b Translations'                                             : pfuncs.extractN00bTranslations,
				'Nakimushi'                                                     : pfuncs.extractNakimushi,
				'Nanjamora'                                                     : pfuncs.extractNanjamora,
				'NanoDesu Light Novel Translations'                             : pfuncs.extractNanoDesuLightNovelTranslations,
				'Nanowave Translations'                                         : pfuncs.extractNanowaveTranslations,
				'National NEET'                                                 : pfuncs.extractNationalNEET,
				'Natsu TL'                                                      : pfuncs.extractNatsuTl,
				'NEET Translations'                                             : pfuncs.extractNeetTranslations,
				'Nega Translations'                                             : pfuncs.extractNegaTranslations,
				'Nekoyashiki'                                                   : pfuncs.extractNekoyashiki,
				'Neo Translations'                                              : pfuncs.extractNeoTranslations,
				'Nepustation'                                                   : pfuncs.extractNepustation,
				'Nightbreeze Translations'                                      : pfuncs.extractNightbreeze,
				'NightFall Translations'                                        : pfuncs.extractNightFallTranslations,
				'NinjaNUF'                                                      : pfuncs.extractNinjaNUF,
				'Nohohon Translation'                                           : pfuncs.extractNohohon,
				'Nooblate'                                                      : pfuncs.extractNooblate,
				'Noodletown Translated'                                         : pfuncs.extractNoodletownTranslated,
				'NOT Daily Translations'                                        : pfuncs.extractNotDailyTranslations,
				'Novel Saga'                                                    : pfuncs.extractNovelSaga,
				'NovelCow'                                                      : pfuncs.extractNovelCow,
				'Novelisation'                                                  : pfuncs.extractNovelisation,
				'Novels Ground'                                                 : pfuncs.extractNovelsGround,
				'Novels Nao'                                                    : pfuncs.extractNovelsNao,
				'NoviceTranslator'                                              : pfuncs.extractNoviceTranslator,
				'Nowhere & Nothing'                                             : pfuncs.extractNowhereNothing,
				'NTRHolic'                                                      : pfuncs.extractNTRHolic,
				'Nutty is Procrastinating'                                      : pfuncs.extractNutty,
				'Ohanashimi'                                                    : pfuncs.extractOhanashimi,
				'OK Translation'                                                : pfuncs.extractOKTranslation,
				'Omega Harem'                                                   : pfuncs.extractOmegaHarem,
				'Omgitsaray Translations'                                       : pfuncs.extractOmgitsaray,
				'One Man Army Translations (OMA)'                               : pfuncs.extractOneManArmy,
				'One Man Army Translations'                                     : pfuncs.extractOneManArmy,
				'One Second Spring'                                             : pfuncs.extractOneSecondSpring,
				'Opinisaya.com'                                                 : pfuncs.extractOpinisaya,
				'Ore ga Heroine in English'                                     : pfuncs.extractOregaHeroineinEnglish,
				'Origin Novels'                                                 : pfuncs.extractOriginNovels,
				'Otome Revolution'                                              : pfuncs.extractOtomeRevolution,
				'otterspacetranslation'                                         : pfuncs.extractOtterspaceTranslation,
				'Outspan Foster'                                                : pfuncs.extractOutspanFoster,
				'Oyasumi Reads'                                                 : pfuncs.extractOyasumiReads,
				'Pact Web Serial'                                               : pfuncs.extractPactWebSerial,
				'pandafuqtranslations'                                          : pfuncs.extractPandafuqTranslations,
				'Patriarch Reliance'                                            : pfuncs.extractPatriarchReliance,
				'Paztok'                                                        : pfuncs.extractPaztok,
				'Pea Translation'                                               : pfuncs.extractPeaTranslation,
				'Pea\'s Kingdom'                                                : pfuncs.extractPeasKingdom,
				'Pekabo Blog'                                                   : pfuncs.extractPekaboBlog,
				'Penguin Overlord Translations'                                 : pfuncs.extractPenguinOverlordTranslations,
				'Pettanko Translations'                                         : pfuncs.extractPettankoTranslations,
				'Pielord Translations'                                          : pfuncs.extractPielordTranslations,
				'Pika Translations'                                             : pfuncs.extractPikaTranslations,
				'Pippi Site'                                                    : pfuncs.extractPippiSite,
				'PlainlyBored'                                                  : pfuncs.extractPlainlyBored,
				'Polyphonic Story Translation Group'                            : pfuncs.extractPolyphonicStoryTranslationGroup,
				'Popsiclete'                                                    : pfuncs.extractPopsiclete,
				'Premium Red Tea'                                               : pfuncs.extractPremiumRedTea,
				'Priddles Translations'                                         : pfuncs.extractPriddlesTranslations,
				'Pride X ReVamp'                                                : pfuncs.extractPrideXReVamp,
				'Prince Revolution!'                                            : pfuncs.extractPrinceRevolution,
				'Project Accelerator'                                           : pfuncs.extractProjectAccelerator,
				'Psicern.Translations'                                          : pfuncs.extractPsicernTranslations,
				'Pumpkin Translations'                                          : pfuncs.extractPumpkinTranslations,
				'putttytranslations'                                            : pfuncs.extractPuttty,
				'Qualidea of Scum and a Gold Coin'                              : pfuncs.extractQualideaofScumandaGoldCoin,
				'QualiTeaTranslations'                                          : pfuncs.extractQualiTeaTranslations,
				'Quality ★ Mistranslations'                                     : pfuncs.extractQualityMistranslations,
				'Radiant Translations'                                          : pfuncs.extractRadiantTranslations,
				'Rainbow Translations'                                          : pfuncs.extractRainbowTranslations,
				'Raising Angels & Defection'                                    : pfuncs.extractRaisingAngelsDefection,
				'Raising the Dead'                                              : pfuncs.extractRaisingTheDead,
				'RANCER'                                                        : pfuncs.extractRancer,
				'Rancer'                                                        : pfuncs.extractRancer,
				'Read Me Translations'                                          : pfuncs.extractReadMeTranslations,
				'Rebirth Online World'                                          : pfuncs.extractRebirthOnlineWorld,
				'Rebirth Online'                                                : pfuncs.extractRebirthOnlineWorld,
				'Red Dragon Translations'                                       : pfuncs.extractRedDragonTranslations,
				'Red Lantern Archives'                                          : pfuncs.extractRedLanternArchives,
				'Reddy Creations'                                               : pfuncs.extractReddyCreations,
				'Reigokai: Isekai Translations'                                 : pfuncs.extractIsekaiTranslations,
				'Reject Hero'                                                   : pfuncs.extractRejectHero,
				'Require: Cookie'                                               : pfuncs.extractRequireCookie,
				'Rhinabolla'                                                    : pfuncs.extractRhinabolla,
				'RidwanTrans'                                                   : pfuncs.extractRidwanTrans,
				'RinOtakuBlog'                                                  : pfuncs.extractRinOtakuBlog,
				'Rip translations'                                              : pfuncs.extractRiptranslations,
				'Rising Dragons Translation'                                    : pfuncs.extractRisingDragons,
				'Roasted Tea'                                                   : pfuncs.extractRoastedTea,
				'Romantic Dreamer\'s Sanctuary'                                 : pfuncs.extractRomanticDreamersSanctuary,
				'Root of Evil'                                                  : pfuncs.extractRootOfEvil,
				'Rosyfantasy - Always Dreaming'                                 : pfuncs.extractRosyfantasy,
				'Roxism HQ'                                                     : pfuncs.extractRoxism,
				'Rumanshi\'s Lair'                                              : pfuncs.extractRumanshisLair,
				'Rumor\'s Block'                                                : pfuncs.extractRumorsBlock,
				'Ruze Translations'                                             : pfuncs.extractRuzeTranslations,
				'Saber Translations'                                            : pfuncs.extractSaberTranslations,
				'Saiaku Translations Blog'                                      : pfuncs.extractSaiakuTranslationsBlog,
				'Sauri\'s TL Blog'                                              : pfuncs.extractSaurisTLBlog,
				'Scrya Translations'                                            : pfuncs.extractScryaTranslations,
				'SenjiQ creations'                                              : pfuncs.extractSenjiQcreations,
				'SETSUNA86BLOG'                                                 : pfuncs.extractSETSUNA86BLOG,
				'Shell2ly C-Novel Site'                                         : pfuncs.extractShell2lyCNovelSite,
				'Sherma Translations'                                           : pfuncs.extractShermaTranslations,
				'Shikkaku Translations'                                         : pfuncs.extractShikkakuTranslations,
				'Shin Sekai Yori – From the New World'                          : pfuncs.extractShinSekaiYori,
				'Shin Translations'                                             : pfuncs.extractShinTranslations,
				'Shinsori Translations'                                         : pfuncs.extractShinsori,
				'Shiroyukineko Translations'                                    : pfuncs.extractShiroyukineko,
				'Shokyuu Translations'                                          : pfuncs.extractShokyuuTranslations,
				'Silent Tl'                                                     : pfuncs.extractSilentTl,
				'Silva\'s Library'                                              : pfuncs.extractSilvasLibrary,
				'Silver Butterfly'                                              : pfuncs.extractSilverButterfly,
				'Sins of the Fathers'                                           : pfuncs.extractSinsOfTheFathers,
				'Skull Squadron'                                                : pfuncs.extractSkullSquadron,
				'Skythewood translations'                                       : pfuncs.extractSkythewood,
				'Sleepy Translations'                                           : pfuncs.extractSleepyTranslations,
				'Slime Lv1'                                                     : pfuncs.extractSlimeLv1,
				'Sloth Translations Blog'                                       : pfuncs.extractSlothTranslationsBlog,
				'Snow & Dust'                                                   : pfuncs.extractSnowDust,
				'Snow Translations'                                             : pfuncs.extractSnowTranslations,
				'Snowy Publications'                                            : pfuncs.extractSnowyPublications,
				'Soaring Translations'                                          : pfuncs.extractSoaring,
				'Solitary Translation'                                          : pfuncs.extractSolitaryTranslation,
				'Solstar24'                                                     : pfuncs.extractSolstar24,
				'Soltarination Scanlations'                                     : pfuncs.extractSoltarinationScanlations,
				'Soojiki\'s Project'                                            : pfuncs.extractSoojikisProject,
				'Sora Translations'                                             : pfuncs.extractSoraTranslations,
				'Sora Translationsblog'                                         : pfuncs.extractSoraTranslations,
				'Sousetsuka'                                                    : pfuncs.extractSousetsuka,
				'Spiritual Transcription'                                       : pfuncs.extractSpiritualTranscription,
				'Spring Scents'                                                 : pfuncs.extractSpringScents,
				'Starrydawn Translations'                                       : pfuncs.extractStarrydawnTranslations,
				'Stellar Transformation Con.'                                   : pfuncs.extractStellarTransformationCon,
				'STL Translations'                                              : pfuncs.extractSTLTranslations,
				'Stone Burners'                                                 : pfuncs.extractStoneBurners,
				'Subudai11'                                                     : pfuncs.extractSubudai11,
				'Sun Shower Fields'                                             : pfuncs.extractSunShowerFields,
				'Super Potato Translations'                                     : pfuncs.extractSuperPotatoTranslations,
				'Supreme Origin Translations'                                   : pfuncs.extractSotranslations,
				'Suteki Da Ne'                                                  : pfuncs.extractSutekiDaNe,
				'Sweet A Collections'                                           : pfuncs.extractSweetACollections,
				'Sword and Game'                                                : pfuncs.extractSwordAndGame,
				'Sylver Translations'                                           : pfuncs.extractSylver,
				'Symbiote'                                                      : pfuncs.extractSymbiote,
				'Taida-dono Translations'                                       : pfuncs.extractTaidadonoTranslations,
				'Taint'                                                         : pfuncs.extractTaint,
				'Tales of MU'                                                   : pfuncs.extractTalesOfMU,
				'Tales of The Forgottenslayer'                                  : pfuncs.extractTalesofTheForgottenslayer,
				'tap-trans » tappity tappity tap.'                              : pfuncs.extractTaptrans,
				'Tarable Translations'                                          : pfuncs.extractTarableTranslations,
				'Tatakau Shisho Light Novel Translation'                        : pfuncs.extractTatakauShishoLightNovelTranslation,
				'Ten Thousand Heaven Controlling Sword'                         : pfuncs.extractTenThousandHeavenControllingSword,
				'Tensai Translations'                                           : pfuncs.extractTensaiTranslations,
				'Tentatively under construction'                                : pfuncs.extractTentativelyUnderconstruction,
				'Terminus Translation'                                          : pfuncs.extractTerminusTranslation,
				'ThatGuyOverThere'                                              : pfuncs.extractThatGuyOverThere,
				'The Asian Cult'                                                : pfuncs.extractTheAsianCult,
				'The Beginning After The End Novel'                             : pfuncs.extractTheBeginningAfterTheEnd,
				'The Beginning After The End'                                   : pfuncs.extractBeginningAfterTheEnd,
				'The C-Novel Project'                                           : pfuncs.extractCNovelProj,
				'The Iron Teeth'                                                : pfuncs.extractTheIronTeeth,
				'The Last Skull'                                                : pfuncs.extractTheLastSkull,
				'The Mustang Translator'                                        : pfuncs.extractTheMustangTranslator,
				'The Named'                                                     : pfuncs.extractTheNamed,
				'The Sphere'                                                    : pfuncs.extractTheSphere,
				'The Tales of Paul Twister'                                     : pfuncs.extractTalesOfPaulTwister,
				'The Zombie Knight'                                             : pfuncs.extractZombieKnight,
				'TheDefend Translations'                                        : pfuncs.extractTheDefendTranslations,
				'TheLazy9'                                                      : pfuncs.extractTheLazy9,
				'This World Work'                                               : pfuncs.extractThisWorldWork,
				'Thunder Translation'                                           : pfuncs.extractThunder,
				'Thyaeria Translations'                                         : pfuncs.extractThyaeria,
				'Tieshaunn'                                                     : pfuncs.extractTieshaunn,
				'tiffybook.com'                                                 : pfuncs.extractCrazyForHENovels,
				'Tinkerbell-san'                                                : pfuncs.extractTinkerbellsan,
				'TL Syosetsu'                                                   : pfuncs.extractTLSyosetsu,
				'Tofubyu'                                                       : pfuncs.extractTofubyu,
				'Tomorolls'                                                     : pfuncs.extractTomorolls,
				'Tony Yon Ka'                                                   : pfuncs.extractTonyYonKa,
				'Totally Insane Tranlation'                                     : pfuncs.extractTotallyInsaneTranslation,
				'Totally Insane Translation'                                    : pfuncs.extractTotallyInsaneTranslation,
				'Totokk\'s Translations'                                        : pfuncs.extractTotokk,
				'Towards the Sky~'                                              : pfuncs.extractTowardsTheSky,
				'Translated by a Clown'                                         : pfuncs.extractClownTrans,
				'Translating For Your Pleasure'                                 : pfuncs.extractTranslatingForYourPleasure,
				'Translating Ze Tian Ji'                                        : pfuncs.extractTranslatingZeTianJi,
				'Translation Nations'                                           : pfuncs.extractTranslationNations,
				'Translation Raven'                                             : pfuncs.extractTranslationRaven,
				'Translation Treasure Box'                                      : pfuncs.extractTranslationTreasureBox,
				'Translations From Outer Space'                                 : pfuncs.extractTranslationsFromOuterSpace,
				'Trinity Archive'                                               : pfuncs.extractTrinityArchive,
				'Tripp Translations'                                            : pfuncs.extractTrippTl,
				'Trung Nguyen'                                                  : pfuncs.extractTrungNguyen,
				'Trungt Nguyen 123'                                             : pfuncs.extractTrungtNguyen,
				'Try Translations'                                              : pfuncs.extractTryTranslations,
				'Tseirp Translations'                                           : pfuncs.extractTseirpTranslations,
				'Tsuigeki Translations'                                         : pfuncs.extractTsuigeki,
				'Tsukigomori'                                                   : pfuncs.extractTsukigomori,
				'Tumble Into Fantasy'                                           : pfuncs.extractTumbleIntoFantasy,
				'Turb0 Translation'                                             : pfuncs.extractTurb0,
				'Turtle and Hare Translations'                                  : pfuncs.extractTurtleandHareTranslations,
				'Tus-Trans'                                                     : pfuncs.extractTusTrans,
				'Twelve Months of May'                                          : pfuncs.extractTwelveMonthsofMay,
				'Twig'                                                          : pfuncs.extractTwig,
				'Twisted Cogs'                                                  : pfuncs.extractTwistedCogs,
				'U Donate We Translate'                                         : pfuncs.extractUDonateWeTranslate,
				'Ultimate Arcane'                                               : pfuncs.extractUltimateArcane,
				'Unchained Translation'                                         : pfuncs.extractUnchainedTranslation,
				'Undecent Translations'                                         : pfuncs.extractUndecentTranslations,
				'Universes With Meaning'                                        : pfuncs.extractUniversesWithMeaning,
				'Unlimited Novel Failures'                                      : pfuncs.extractUnlimitedNovelFailures,
				'Unlimited Story Works'                                         : pfuncs.extractUnlimitedStoryWorks,
				'unnamedtranslations.blogspot.com'                              : pfuncs.extractUnnamedtranslations,
				'Untuned Translation Blog'                                      : pfuncs.extractUntunedTranslation,
				'Useless no 4'                                                  : pfuncs.extractUselessno4,
				'VaanCruze'                                                     : pfuncs.extractMaouTheYuusha,
				'Verathragana Stories'                                          : pfuncs.extractVerathragana,
				'Village Translations'                                          : pfuncs.extractVillageTranslations,
				'Void Translations'                                             : pfuncs.extractVoidTranslations,
				'Volare Translations'                                           : pfuncs.extractVolareTranslations,
				'Walk the Jiang Hu'                                             : pfuncs.extractWalkTheJiangHu,
				'Walking the Storm'                                             : pfuncs.extractWalkingTheStorm,
				'Wat Da Meow'                                                   : pfuncs.extractWatDaMeow,
				'Watermelon Helmets'                                            : pfuncs.extractWatermelonHelmets,
				'WCC Translation'                                               : pfuncs.extractWCCTranslation,
				'Weaving stories and building castles in the clouds'            : pfuncs.extractWeavingstoriesandbuildingcastlesintheclouds,
				'Web Novel Japanese Translation'                                : pfuncs.extractWebNovelJapaneseTranslation,
				'Welcome To The Underdark'                                      : pfuncs.extractWelcomeToTheUnderdark,
				'Wele Translation'                                              : pfuncs.extractWeleTranslation,
				'When The Hunting Party Came'                                   : pfuncs.extractWhenTheHuntingPartyCame,
				'Whimsical Land'                                                : pfuncs.extractWhimsicalLand,
				'White Tiger Translations'                                      : pfuncs.extractWhiteTigerTranslations,
				'Willful Casual'                                                : pfuncs.extractWillfulCasual,
				'Witch Life Novel'                                              : pfuncs.extractWitchLife,
				'WL Translations'                                               : pfuncs.extractWLTranslations,
				'Wolfie Translation'                                            : pfuncs.extractWolfieTranslation,
				'Word of Craft'                                                 : pfuncs.extractWordofCraft,
				'World of Summie'                                               : pfuncs.extractWorldofSummie,
				'World of Watermelons'                                          : pfuncs.extractWatermelons,
				'Worm - A Complete Web Serial'                                  : pfuncs.extractWormACompleteWebSerial,
				'Wuxia Heroes'                                                  : pfuncs.extractWuxiaHeroes,
				'Wuxia Translations'                                            : pfuncs.extractWuxiaTranslations,
				'Wuxia Translators'                                             : pfuncs.extractWuxiaTranslators,
				'WuxiaSociety'                                                  : pfuncs.extractWuxiaSociety,
				'Wuxiaworld'                                                    : pfuncs.extractWuxiaworld,
				'Wuxiwish'                                                      : pfuncs.extractWuxiwish,
				'www.pridesfamiliarsmaidens.com'                                : pfuncs.extractPridesFamiliarsMaidens,
				'www.soltarination.org'                                         : pfuncs.extractSoltarination,
				'Xant & Minions'                                                : pfuncs.extractXantAndMinions,
				'Xant Does Stuff and Things'                                    : pfuncs.extractXantDoesStuffAndThings,
				'xantbos.wordpress.com'                                         : pfuncs.extractXantbos,
				'Yet Another Translation Site'                                  : pfuncs.extractMiaomix539,
				'Yi Yue Translation'                                            : pfuncs.extractYiYueTranslation,
				'Yoraikun Translation'                                          : pfuncs.extractYoraikun,
				'Youjinsite Translations'                                       : pfuncs.extractYoujinsite,
				'Youko Advent'                                                  : pfuncs.extractYoukoAdvent,
				'Youshoku Translations'                                         : pfuncs.extractYoushoku,
				'youtsubasilver\'s Blog'                                        : pfuncs.extractYoutsubasilversBlog,
				'Yukkuri Free Time Literature Service'                          : pfuncs.extractYukkuri,
				'Zen Translations'                                              : pfuncs.extractZenTranslations,
				'Zeonic'                                                        : pfuncs.extractZeonic,
				'Ziru\'s Musings | Translations~'                               : pfuncs.extractZiruTranslations,
				'ZSW'                                                           : pfuncs.extractZSW,
				'~Taffy Translations~'                                          : pfuncs.extractTaffyTranslations,

				'ℝeanとann@'                                                     : pfuncs.extractReantoAnna,
				'「\u3000」'                                                      : pfuncs.extractU3000,
				'お兄ちゃん、やめてぇ！'                                               : pfuncs.extractOniichanyamete,
				'ヾ(。￣□￣)ﾂ'                                                    : pfuncs.extractAngry,
				'一期一会, 万歳!'                                                 : pfuncs.extract一期一会万歳,
				'中翻英圖書館 Translations'                                       : pfuncs.extractTuShuGuan,
				'天才創造すなわち百合'                                               : pfuncs.extract天才創造すなわち百合,
				'桜翻訳! | Light novel translations'                             : pfuncs.extractSakurahonyaku,
				'睡眠中毒'                                                        : pfuncs.extract睡眠中毒,
				'輝く世界'                                                        : pfuncs.extract輝く世界,



				# KnW mess
				'Blazing Translations'                                          : pfuncs.extractKnW,
				'CapsUsingShift Tl'                                             : pfuncs.extractKnW,
				'Insignia Pierce'                                               : pfuncs.extractKnW,
				'Konjiki no Wordmaster'                                         : pfuncs.extractKnW,
				'Loliquent'                                                     : pfuncs.extractKnW,
				'Pummels Translations'                                          : pfuncs.extractKnW,

				'Kiriko Translations'                                           : pfuncs.extractKirikoTranslations,
				'XCrossJ'                                                       : pfuncs.extractXCrossJ,
				# No Posts yet?
				'Novel Trans'                                                   : pfuncs.extractNovelTrans,
				'The Bathrobe Knight'                                           : pfuncs.extractBathrobeKnight,
				'Dramas, Books & Tea'                                           : pfuncs.extractDramasBooksTea,

				# Not parseable.
				'Crack of Dawn Translations'                                    : pfuncs.extractCrackofDawnTranslations,


		}

		# ('Have Func', False), ('SourceName', 'sparklingdawnlights.blogspot.com'),

		# ('Have Func', False), ('SourceName', 'Zeonic'),
		# ('Have Func', False), ('SourceName', '「\u3000」'),
		# ('Have Func', False), ('SourceName', '天才創造すなわち百合'),

		# 'n00btranslations.wordpress.com'                                : pfuncs.extractN00btranslations.wordpress.com,
		# 'omatranslations.wordpress.com'                                 : pfuncs.extractOmatranslations.wordpress.com,
		# 'soaringtranslations.wordpress.com'                             : pfuncs.extractSoaringtranslations.wordpress.com,
		# 'solitarytranslation.wordpress.com'                             : pfuncs.extractSolitarytranslation.wordpress.com,
		# 'walkthejianghu.wordpress.com'                                  : pfuncs.extractWalkthejianghu.wordpress.com,


		if item['srcname'] in funcMap:
			ret = funcMap[item['srcname']](item)
		else:
			print("No filter found for '%s'?" % item['srcname'])

		# NanoDesu is annoying and makes their releases basically impossible to parse. FFFUUUUUu
		if "(NanoDesu)" in item['srcname'] and not ret:
			return False

		if (flags.RSS_DEBUG or self.dbg_print) and self.write_debug and ret == False and not "teaser" in item['title'].lower():
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if vol or chp or frag and not flags.RSS_DEBUG:

				with open('rss_filter_misses-1.json', "a") as fp:

					write_items = {
						"SourceName" : item['srcname'],
						"Title"      : item['title'],
						"Tags"       : list(item['tags']),
						"Vol"        : False if not vol else vol,
						"Chp"        : False if not chp else chp,
						"Frag"       : False if not frag else frag,
						"Postfix"    : postfix,
						"Feed URL"   : item['linkUrl'],
						"GUID"       : item['guid'],
						"Have Func"  : item['srcname'] in funcMap,
					}

					# fp.write("\n==============================\n")
					# fp.write("Feed URL: '%s', guid: '%s'" % (item['linkUrl'], item['guid']))
					# fp.write("'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'\n" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix, item['linkUrl']))

					fp.write("%s" % (json.dumps(write_items, )))
					fp.write("\n")

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if self.dbg_print or flags.RSS_DEBUG:
			# False means not caught. None means intentionally ignored.

			if ret == False and (vol or chp or frag) and not "teaser" in item['title'].lower():
				print("Missed: '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))
			elif ret:
				pass
				# print("OK! '%s', V:'%s', C:'%s', '%s', '%s', '%s'" % (ret['srcname'], ret['vol'], ret['chp'], ret['postfix'], ret['series'], item['title']))
			else:
				pass
				# print("Wat: '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix, item['linkUrl']))

			if flags.RSS_DEBUG:
				ret = False

		# Only return a value if we've actually found a chapter/vol
		if ret and not (ret['vol'] or ret['chp'] or ret['postfix']):
			self.log.info("Skipping item due to no chapter/vol/postfix: '%s', '%s', '%s', '%s', '%s', '%s', '%s'", item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix)
			ret = False

		# Do not trigger if there is "preview" in the title.
		if 'preview' in item['title'].lower():
			self.log.info("Skipping item due to preview string: '%s', '%s', '%s', '%s', '%s', '%s', '%s'", item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix)
			ret = False
		if ret:
			assert 'tl_type' in ret


		if ret == None:
			ret = False


		return ret


	def getProcessedReleaseInfo(self, feedDat):

		if any([item in feedDat['linkUrl'] for item in skip_filter]):
			print("Skipping!")
			return


		release = self.dispatchRelease(feedDat)

		if release:
			ret = {
				'type' : 'parsed-release',
				'data' : release
			}
			return json.dumps(ret)
		return False


	def getRawFeedMessage(self, feedDat):

		feedDat = feedDat.copy()

		# remove the contents item, since it can be
		# quite large, and is not used.
		feedDat.pop('contents')
		ret = {
			'type' : 'raw-feed',
			'data' : feedDat
		}
		try:
			return json.dumps(ret)
		except TypeError:
			return None

	def processFeedData(self, feedDat, tx_raw=True, tx_parse=True):

		if any([item in feedDat['linkUrl'] for item in skip_filter]):
			print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return


		netloc = urllib.parse.urlparse(feedDat['linkUrl']).netloc

		nicename = feedNameLut.getNiceName(feedDat['linkUrl'])
		if not nicename:
			nicename = netloc
		feedDat['srcname'] = nicename

		# print("ProcessFeedData! ", netloc)
		if not WebMirror.rules.netloc_send_feed(netloc):
			print("Not sending data for netloc: ", netloc)
			return

		raw = self.getRawFeedMessage(feedDat)
		new = self.getProcessedReleaseInfo(feedDat)

		if tx_raw:
			if raw:
				self.amqp_put_item(raw)
		if tx_parse:
			if new:
				self.amqp_put_item(new)

