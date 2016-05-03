
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import json
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut


import WebMirror.OutputFilters.rss.ParserFuncs_a_g as pfuncs_a_g
import WebMirror.OutputFilters.rss.ParserFuncs_h_n as pfuncs_h_n
import WebMirror.OutputFilters.rss.ParserFuncs_o_u as pfuncs_o_u
import WebMirror.OutputFilters.rss.ParserFuncs_stub as pfuncs_stub
import WebMirror.OutputFilters.rss.ParserFuncs_v_other as pfuncs_v_other

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
	'pokegirls.org',
	'www.asstr.org',
	'www.mcstories.com',
	'www.novelupdates.com',
	'40pics.com',

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

				'A0132'                                                         : pfuncs_a_g.extractA0132,
				'Adamantine Dragon in the Crystal World'                        : pfuncs_a_g.extractAdamantineDragonintheCrystalWorld,
				'AFlappyTeddyBird'                                              : pfuncs_a_g.extractAFlappyTeddyBird,
				'A Grey World'                                                  : pfuncs_a_g.extractAGreyWorld,
				'Albert Kenoreijou'                                             : pfuncs_a_g.extractAlbertKenoreijou,
				'Alcsel Translations'                                           : pfuncs_a_g.extractAlcsel,
				'Alice Translations'                                            : pfuncs_a_g.extractAliceTranslations,
				'alicetranslations.wordpress.com'                               : pfuncs_a_g.extractAlicetranslations,
				'All\'s Fair In Love & War'                                     : pfuncs_a_g.extractAllsFairInLoveWar,
				'Altoroc Translations'                                          : pfuncs_a_g.extractAltorocTranslations,
				'Alyschu & Co'                                                  : pfuncs_a_g.extractAlyschuCo,
				'Amery Edge'                                                    : pfuncs_a_g.extractAmeryEdge,
				'Anathema Serial'                                               : pfuncs_a_g.extractAnathema,
				'Andrew9495\'s MTL corner'                                      : pfuncs_a_g.extractAndrew9495,
				'ヾ(。￣□￣)ﾂ'                                                    : pfuncs_a_g.extractAngry,
				'Anne And Cindy'                                                : pfuncs_a_g.extractAnneAndCindy,
				'Anon Empire'                                                   : pfuncs_a_g.extractAnonEmpire,
				'Another Parallel World'                                        : pfuncs_a_g.extractAnotherParallelWorld,
				'Another World Translations'                                    : pfuncs_a_g.extractAnotherWorldTranslations,
				'Aori Translations'                                             : pfuncs_a_g.extractAoriTranslations,
				'A Pearly View'                                                 : pfuncs_a_g.extractAPearlyView,
				'Aquarilas\' Scenario'                                          : pfuncs_a_g.extractAquarilasScenario,
				'Aqua Scans'                                                    : pfuncs_a_g.extractAquaScans,
				'Aran Translations'                                             : pfuncs_a_g.extractAranTranslations,
				'Archivity'                                                     : pfuncs_a_g.extractArchivity,
				'Ares Novels'                                                   : pfuncs_a_g.extractAresNovels,
				'Ark Machine Translations'                                      : pfuncs_a_g.extractArkMachineTranslations,
				'asd398'                                                        : pfuncs_a_g.extractAsd398,
				'AsherahBlue\'s Notebook'                                       : pfuncs_a_g.extractAsherahBlue,
				'Aten Translations'                                             : pfuncs_a_g.extractAtenTranslations,
				'A Translator\'s Ramblings'                                     : pfuncs_a_g.extractATranslatorsRamblings,
				'A traveler\'s translations.'                                   : pfuncs_a_g.extractATravelersTranslations,
				'Avert Translations'                                            : pfuncs_a_g.extractAvert,
				'Ayax World'                                                    : pfuncs_a_g.extractAyaxWorld,
				'Azure Sky Translation'                                         : pfuncs_a_g.extractAzureSky,
				'Azurro 4 Cielo'                                                : pfuncs_a_g.extractAzurro,
				'Bad Translation'                                               : pfuncs_a_g.extractBadTranslation,
				'Baka Dogeza Translation'                                       : pfuncs_a_g.extractBakaDogeza,
				'Baka Pervert'                                                  : pfuncs_a_g.extractBakaPervert,
				"'Ball'-Kicking Gang Boss"                                      : pfuncs_a_g.extractBallKickingGangBoss,
				'The Bathrobe Knight'                                           : pfuncs_a_g.extractBathrobeKnight,
				'Bayabusco Translation'                                         : pfuncs_a_g.extractBayabuscoTranslation,
				'Bcat00 Translation'                                            : pfuncs_a_g.extractBcat00,
				'Bear Bear Translations'                                        : pfuncs_a_g.extractBearBearTranslations,
				'Beehugger'                                                     : pfuncs_a_g.extractBeehugger,
				'The Beginning After The End'                                   : pfuncs_a_g.extractBeginningAfterTheEnd,
				'Berseker Translations'                                         : pfuncs_a_g.extractBersekerTranslations,
				'BeRsErk Translations'                                          : pfuncs_a_g.extractBeRsErkTranslations,
				'Bijinsans'                                                     : pfuncs_a_g.extractBijinsans,
				'Binggo&Corp'                                                   : pfuncs_a_g.extractBinggoCorp,
				'Binhjamin'                                                     : pfuncs_a_g.extractBinhjamin,
				'Blade of Hearts'                                               : pfuncs_a_g.extractBladeOfHearts,
				'Blublub'                                                       : pfuncs_a_g.extractBlublub,
				'Bluefire Translations'                                         : pfuncs_a_g.extractBluefireTranslations,
				'Blue Silver Translations'                                      : pfuncs_a_g.extractBlueSilverTranslations,
				'Books Movies and Beyond'                                       : pfuncs_a_g.extractBooksMoviesAndBeyond,
				'Bruin Translation'                                             : pfuncs_a_g.extractBruinTranslation,
				'Bu Bu Jing Xin Translation'                                    : pfuncs_a_g.extractBuBuJingXinTrans,
				'Burei Dan Works'                                               : pfuncs_a_g.extractBureiDan,
				'Calico x Tabby'                                                : pfuncs_a_g.extractCalicoxTabby,
				'Cas Project Site'                                              : pfuncs_a_g.extractCasProjectSite,
				'Cat Scans'                                                     : pfuncs_a_g.extractCatScans,
				"Cautr's"                                                       : pfuncs_a_g.extractCautrs,
				'CaveScans'                                                     : pfuncs_a_g.extractCaveScans,
				'cavescans.com'                                                 : pfuncs_a_g.extractCavescans,
				'C.E. Light Novel Translations'                                 : pfuncs_a_g.extractCeLn,
				'Ceruleonice Translations'                                      : pfuncs_a_g.extractCeruleonice,
				'Cheddar!'                                                      : pfuncs_a_g.extractCheddar,
				'Chinese BL Translations'                                       : pfuncs_a_g.extractChineseBLTranslations,
				'Chinese Weaboo Translations'                                   : pfuncs_a_g.extractChineseWeabooTranslations,
				'Chrona Zero'                                                   : pfuncs_a_g.extractChronaZero,
				'Chronon Translations'                                          : pfuncs_a_g.extractChrononTranslations,
				'ChubbyCheeks'                                                  : pfuncs_a_g.extractChubbyCheeks,
				'Circle of Shards'                                              : pfuncs_a_g.extractCircleofShards,
				'Circus Translations'                                           : pfuncs_a_g.extractCircusTranslations,
				'Clicky Click Translation'                                      : pfuncs_a_g.extractClicky,
				'Cloud Manor'                                                   : pfuncs_a_g.extractCloudManor,
				'Cloud Translations'                                            : pfuncs_a_g.extractCloudTranslations,
				'Clover\'s Nook'                                                : pfuncs_a_g.extractCloversNook,
				'Translated by a Clown'                                         : pfuncs_a_g.extractClownTrans,
				'The C-Novel Project'                                           : pfuncs_a_g.extractCNovelProj,
				'C Novels 2 C'                                                  : pfuncs_a_g.extractCNovels2C,
				'C-Novel Tranlations…'                                          : pfuncs_a_g.extractCNovelTranlations,
				'Code-Zero\'s Blog'                                             : pfuncs_a_g.extractCodeZerosBlog,
				'CookiePasta'                                                   : pfuncs_a_g.extractCookiePasta,
				'CookiePasta Translations'                                      : pfuncs_a_g.extractCookiePastaTranslations,
				'Cosmic Translation'                                            : pfuncs_a_g.extractCosmicTranslation,
				'Crack of Dawn Translations'                                    : pfuncs_a_g.extractCrackofDawnTranslations,
				'Crappy Machine Translation'                                    : pfuncs_a_g.extractCrappyMachineTranslation,
				'Crazy for HE Novels'                                           : pfuncs_a_g.extractCrazyForHENovels,
				'tiffybook.com'                                                 : pfuncs_a_g.extractCrazyForHENovels,
				'CrystalRainDescends'                                           : pfuncs_a_g.extractCrystalRainDescends,
				'CtrlAlcalá'                                                    : pfuncs_a_g.extractCtrlAlcala,
				'Currently TLing [Bu ni Mi]'                                    : pfuncs_a_g.extractCurrentlyTLingBuniMi,
				'DadIsHero Fan Translations'                                    : pfuncs_a_g.extractDadIsHeroFanTranslations,
				'Daily-Dallying'                                                : pfuncs_a_g.extractDailyDallying,
				'Dao Seeker Blog'                                               : pfuncs_a_g.extractDaoSeekerBlog,
				'A fish once said this to me'                                   : pfuncs_a_g.extractDarkFish,
				'Dark Translations'                                             : pfuncs_a_g.extractDarkTranslations,
				'Dawning Howls'                                                 : pfuncs_a_g.extractDawningHowls,
				'Deadly Forgotten Legends'                                      : pfuncs_a_g.extractDeadlyForgottenLegends,
				'Defan\'s Translations'                                         : pfuncs_a_g.extractDefansTranslations,
				'Defiring'                                                      : pfuncs_a_g.extractDefiring,
				'Dekinai Diary'                                                 : pfuncs_a_g.extractDekinaiDiary,
				'Delicious Translations'                                        : pfuncs_a_g.extractDeliciousTranslations,
				'Demerith Translation'                                          : pfuncs_a_g.extractDemerithTranslation,
				'Descent Subs'                                                  : pfuncs_a_g.extractDescentSubs,
				'Dewey Night Unrolls'                                           : pfuncs_a_g.extractDeweyNightUnrolls,
				'DHH Translations'                                              : pfuncs_a_g.extractDHHTranslations,
				'Disappointing Translations'                                    : pfuncs_a_g.extractDisappointingTranslations,
				'Distracted Chinese'                                            : pfuncs_a_g.extractDistractedChinese,
				'Distracted Translations'                                       : pfuncs_a_g.extractDistractedTranslations,
				'Diwasteman'                                                    : pfuncs_a_g.extractDiwasteman,
				'DokuHana Translations'                                         : pfuncs_a_g.extractDokuHanaTranslations,
				'Dorayakiz'                                                     : pfuncs_a_g.extractDorayakiz,
				"DOW's Translations"                                            : pfuncs_a_g.extractDOWsTranslations,
				'DragomirCM'                                                    : pfuncs_a_g.extractDragomirCM,
				'Dragon MT'                                                     : pfuncs_a_g.extractDragonMT,
				'Dramas, Books & Tea'                                           : pfuncs_a_g.extractDramasBooksTea,
				'Dreadful Decoding'                                             : pfuncs_a_g.extractDreadfulDecoding,
				'Dream Avenue'                                                  : pfuncs_a_g.extractDreamAvenue,
				"Dreamless Window's translation"                                : pfuncs_a_g.extractDreamlessWindowsTranslation,
				'Dreams of Jianghu'                                             : pfuncs_a_g.extractDreamsOfJianghu,
				'Ducky\'s English Translations'                                 : pfuncs_a_g.extractDuckysEnglishTranslations,
				'Duran Daru Translation'                                        : pfuncs_a_g.extractDuranDaruTranslation,
				'Durasama'                                                      : pfuncs_a_g.extractDurasama,
				'Dynamis Gaul Light Novel'                                      : pfuncs_a_g.extractDynamisGaul,
				'EccentricTranslations'                                         : pfuncs_a_g.extractEccentricTranslations,
				'EC Webnovel'                                                   : pfuncs_a_g.extractECWebnovel,
				'ELYSION Translation'                                           : pfuncs_a_g.extractELYSIONTranslation,
				'Emergency Exit\'s Release Blog'                                : pfuncs_a_g.extractEmergencyExitsReleaseBlog,
				'Emruyshit Translations'                                        : pfuncs_a_g.extractEmruyshitTranslations,
				'EndKun'                                                        : pfuncs_a_g.extractEndKun,
				'End Online Novel'                                              : pfuncs_a_g.extractEndOnline,
				'Ensig\'s Writings'                                             : pfuncs_a_g.extractEnsigsWritings,
				'Ensj Translations'                                             : pfuncs_a_g.extractEnsjTranslations,
				'Ente38 translations'                                           : pfuncs_a_g.extractEnte38translations,
				'EnTruce Translations'                                          : pfuncs_a_g.extractEnTruceTranslations,
				'Epithetic'                                                     : pfuncs_a_g.extractEpithetic,
				'Epyon Translations'                                            : pfuncs_a_g.extractEpyonTranslations,
				'Ero Light Novel Translations'                                  : pfuncs_a_g.extractEroLightNovelTranslations,
				'Eros Workshop'                                                 : pfuncs_a_g.extractErosWorkshop,
				'eternalpath.net'                                               : pfuncs_a_g.extractEternalpath,
				'Etheria Translations'                                          : pfuncs_a_g.extractEtheriaTranslations,
				'Eugene Rain'                                                   : pfuncs_a_g.extractEugeneRain,
				"Evida's Indo Romance"                                          : pfuncs_a_g.extractEvidasIndoRomance,
				'Eye of Adventure '                                             : pfuncs_a_g.extractEyeofAdventure,
				'EZ Translations'                                               : pfuncs_a_g.extractEZTranslations,
				'Fake typist'                                                   : pfuncs_a_g.extractFaketypist,
				'Fak Translations'                                              : pfuncs_a_g.extractFakTranslations,
				'Falamar Translation'                                           : pfuncs_a_g.extractFalamarTranslation,
				'Falinmer'                                                      : pfuncs_a_g.extractFalinmer,
				'Fanatical'                                                     : pfuncs_a_g.extractFanatical,
				'FeedProxy'                                                     : pfuncs_a_g.extractFeedProxy,
				'fgiLaN translations'                                           : pfuncs_a_g.extractfgiLaNTranslations,
				'Fighting Dreamers Scanlations'                                 : pfuncs_a_g.extractFightingDreamersScanlations,
				'Firebird\'s Nest'                                              : pfuncs_a_g.extractFirebirdsNest,
				'Five Star Specialists'                                         : pfuncs_a_g.extractFiveStar,
				'Flicker Hero'                                                  : pfuncs_a_g.extractFlickerHero,
				'Flower Bridge Too'                                             : pfuncs_a_g.extractFlowerBridgeToo,
				'Forgetful Dreamer'                                             : pfuncs_a_g.extractForgetfulDreamer,
				'Forgotten Conqueror'                                           : pfuncs_a_g.extractForgottenConqueror,
				'/'                                                             : pfuncs_a_g.extractForwardSlash,
				'Frostfire 10'                                                  : pfuncs_a_g.extractFrostfire10,
				'Fudge Translations'                                            : pfuncs_a_g.extractFudgeTranslations,
				'Fung Shen'                                                     : pfuncs_a_g.extractFungShen,
				'Fuzion Life'                                                   : pfuncs_a_g.extractFuzionLife,
				'Gaochao Translations'                                          : pfuncs_a_g.extractGaochaoTranslations,
				'Gargoyle Web Serial'                                           : pfuncs_a_g.extractGargoyleWebSerial,
				'Gila Translation Monster'                                      : pfuncs_a_g.extractGilaTranslation,
				'Giraffe Corps'                                                 : pfuncs_a_g.extractGiraffe,
				'[G.O] Chronicles'                                              : pfuncs_a_g.extractGOChronicles,
				'Goddess! Grant Me a Girlfriend!!'                              : pfuncs_a_g.extractGoddessGrantMeaGirlfriend,
				'Gravity Tales'                                                 : pfuncs_a_g.extractGravityTranslation,
				'GrimdarkZ Translations'                                        : pfuncs_a_g.extractGrimdarkZTranslations,
				'Grow with Me'                                                  : pfuncs_a_g.extractGrowWithMe,
				'Grow with me'                                                  : pfuncs_a_g.extractGrowWithMe,
				'guhehe.TRANSLATIONS'                                           : pfuncs_a_g.extractGuhehe,
				'Guro Translation'                                              : pfuncs_a_g.extractGuroTranslation,
				'Hajiko translation'                                            : pfuncs_h_n.extractHajiko,
				'Hamster428'                                                    : pfuncs_h_n.extractHamster428,
				'HaruPARTY'                                                     : pfuncs_h_n.extractHaruPARTY,
				'Heart Crusade Scans'                                           : pfuncs_h_n.extractHeartCrusadeScans,
				'Helidwarf'                                                     : pfuncs_h_n.extractHelidwarf,
				'Hello Translations'                                            : pfuncs_h_n.extractHelloTranslations,
				'Hellping'                                                      : pfuncs_h_n.extractHellping,
				'Hell Yeah 524'                                                 : pfuncs_h_n.extractHellYeah524,
				'Hendricksen-sama'                                              : pfuncs_h_n.extractHendricksensama,
				'Henouji Translation'                                           : pfuncs_h_n.extractHenoujiTranslation,
				'Heroic Legend of Arslan Translations'                          : pfuncs_h_n.extractHeroicLegendOfArslanTranslations,
				'Heroic Novels'                                                 : pfuncs_h_n.extractHeroicNovels,
				'Hikki no Mori Translations'                                    : pfuncs_h_n.extractHikkinoMoriTranslations,
				'Hokage Translations'                                           : pfuncs_h_n.extractHokageTrans,
				'Hold \'X\' and Click'                                          : pfuncs_h_n.extractHoldX,
				"Hon'yaku"                                                      : pfuncs_h_n.extractHonyaku,
				'Hot Cocoa Translations'                                        : pfuncs_h_n.extractHotCocoa,
				"Hugs & Love"                                                   : pfuncs_h_n.extractHugsAndLove,
				'Hyorinmaru Blog'                                               : pfuncs_h_n.extractHyorinmaruBlog,
				'Hyorinmaru'                                                    : pfuncs_h_n.extractHyorinmaruBlog,
				'Imoutolicious Light Novel Translations'                        : pfuncs_h_n.extractImoutolicious,
				'Infinite Novel Translations'                                   : pfuncs_h_n.extractInfiniteNovelTranslations,
				'Infinite Translations'                                         : pfuncs_h_n.extractInfiniteTranslations,
				'IntenseDesSugar'                                               : pfuncs_h_n.extractIntenseDesSugar,
				'Isekai Mahou Translations!'                                    : pfuncs_h_n.extractIsekaiMahou,
				'Isekai Soul-Cyborg Translations'                               : pfuncs_h_n.extractIsekaiTranslation,
				'Reigokai: Isekai Translations'                                 : pfuncs_h_n.extractIsekaiTranslations,
				'Isolarium'                                                     : pfuncs_h_n.extractIsolarium,
				'Istian\'s Workshop'                                            : pfuncs_h_n.extractIstiansWorkshop,
				'Iterations within a Thought-Eclipse'                           : pfuncs_h_n.extractIterations,
				'itranslateln'                                                  : pfuncs_h_n.extractItranslateln,
				'izra709 | B Group no Shounen Translations'                     : pfuncs_h_n.extractIzra709,
				'Jagaimo'                                                       : pfuncs_h_n.extractJagaimo,
				'Januke Translations'                                           : pfuncs_h_n.extractJanukeTranslations,
				'Japtem'                                                        : pfuncs_h_n.extractJaptem,
				'JawzTranslations'                                              : pfuncs_h_n.extractJawzTranslations,
				'Joeglen\'s Translation Space'                                  : pfuncs_h_n.extractJoeglensTranslationSpace,
				'Joie de Vivre'                                                 : pfuncs_h_n.extractJoiedeVivre,
				'Jun Juntianxia'                                                : pfuncs_h_n.extractJunJuntianxia,
				'Kaezar Translations'                                           : pfuncs_h_n.extractKaezar,
				'Kahoim Translations'                                           : pfuncs_h_n.extractKahoim,
				'Kakkokari'                                                     : pfuncs_h_n.extractKakkokari,
				'Kami Translation'                                              : pfuncs_h_n.extractKamiTranslation,
				'Kawaii Daikon'                                                 : pfuncs_h_n.extractKawaiiDaikon,
				'Kedelu'                                                        : pfuncs_h_n.extractKedelu,
				'Kerambit\'s Incisions'                                         : pfuncs_h_n.extractKerambit,
				'Keyo Translations'                                             : pfuncs_h_n.extractKeyoTranslations,
				'King Jaahn\'s Subjects'                                        : pfuncs_h_n.extractKingJaahn,
				'Kiri Leaves'                                                   : pfuncs_h_n.extractKiri,
				'Kiriko Translations'                                           : pfuncs_h_n.extractKirikoTranslations,
				'Kisato\'s MLTs'                                                : pfuncs_h_n.extractKisatosMLTs,
				'Knokkro Translations'                                          : pfuncs_h_n.extractKnokkroTranslations,
				'KN Translation'                                                : pfuncs_h_n.extractKNTranslation,
				'Blazing Translations'                                          : pfuncs_h_n.extractKnW,
				'CapsUsingShift Tl'                                             : pfuncs_h_n.extractKnW,
				'Insignia Pierce'                                               : pfuncs_h_n.extractKnW,
				'Konjiki no Wordmaster'                                         : pfuncs_h_n.extractKnW,
				'Loliquent'                                                     : pfuncs_h_n.extractKnW,
				'Pummels Translations'                                          : pfuncs_h_n.extractKnW,
				'KobatoChanDaiSukiScan'                                         : pfuncs_h_n.extractKobatoChanDaiSukiScan,
				'Kokuma Translations'                                           : pfuncs_h_n.extractKokumaTranslations,
				'KONDEE Translations'                                           : pfuncs_h_n.extractKONDEETranslations,
				'Konobuta'                                                      : pfuncs_h_n.extractKonobuta,
				'Koong Koong Translations'                                      : pfuncs_h_n.extractKoongKoongTranslations,
				'Korean Novel Translations'                                     : pfuncs_h_n.extractKoreanNovelTrans,
				'Kore Yori Hachidori'                                           : pfuncs_h_n.extractKoreYoriHachidori,
				'Krytyk\'s Translations'                                        : pfuncs_h_n.extractKrytyksTranslations,
				'Kuma Otou'                                                     : pfuncs_h_n.extractKumaOtou,
				'Kuro Translations'                                             : pfuncs_h_n.extractKuroTranslations,
				'Kurotsuki Novel'                                               : pfuncs_h_n.extractKurotsukiNovel,
				'Kyakka'                                                        : pfuncs_h_n.extractKyakka,
				'Kyakka Translations'                                           : pfuncs_h_n.extractKyakkaTranslations,
				'kyoptionslibrary.blogspot.com'                                 : pfuncs_h_n.extractKyoptionslibrary,
				'L2M'                                                           : pfuncs_h_n.extractL2M,
				'Larvyde'                                                       : pfuncs_h_n.extractLarvyde,
				'Lascivious Imouto'                                             : pfuncs_h_n.extractLasciviousImouto,
				'Lastvoice Translator'                                          : pfuncs_h_n.extractLastvoiceTranslator,
				'Layzisheep'                                                    : pfuncs_h_n.extractLayzisheep,
				'Legend of Galactic Heroes Translation Project'                 : pfuncs_h_n.extractLegendofGalacticHeroes,
				'Lickymee Translations'                                         : pfuncs_h_n.extractLickymeeTranslations,
				'Light Novels Translations'                                     : pfuncs_h_n.extractLightNovelsTranslations,
				'Light Novel translations'                                      : pfuncs_h_n.extractLightNoveltranslations,
				'Lil\' Bliss Novels'                                            : pfuncs_h_n.extractLilBlissNovels,
				'Lingson\'s Translations'                                       : pfuncs_h_n.extractLingson,
				'Ling Translates Sometimes'                                     : pfuncs_h_n.extractLingTranslatesSometimes,
				'Linked Translations'                                           : pfuncs_h_n.extractLinkedTranslations,
				'Little Novel Translation'                                      : pfuncs_h_n.extractLittleNovelTranslation,
				'LittleShanks Translations'                                     : pfuncs_h_n.extractLittleShanksTranslations,
				'Little Translations'                                           : pfuncs_h_n.extractLittleTranslations,
				'Lizard Translations'                                           : pfuncs_h_n.extractLizardTranslations,
				'LMS Machine Translations'                                      : pfuncs_h_n.extractLMSMachineTranslations,
				'Ln Addiction'                                                  : pfuncs_h_n.extractLnAddiction,
				'Lohithbb TLs'                                                  : pfuncs_h_n.extractLohithbbTLs,
				'Loiterous'                                                     : pfuncs_h_n.extractLoiterous,
				'Lonahora'                                                      : pfuncs_h_n.extractLonahora,
				'LorCromwell'                                                   : pfuncs_h_n.extractLorCromwell,
				'LordofScrubs'                                                  : pfuncs_h_n.extractLordofScrubs,
				'Lost in Translation'                                           : pfuncs_h_n.extractLostInTranslation,
				'Luen Translations'                                             : pfuncs_h_n.extractLuenTranslations,
				'Lunaris'                                                       : pfuncs_h_n.extractLunaris,
				'Lunate'                                                        : pfuncs_h_n.extractLunate,
				'LygarTranslations'                                             : pfuncs_h_n.extractLygarTranslations,
				'Lylis Translations'                                            : pfuncs_h_n.extractLylisTranslations,
				'Lynfamily'                                                     : pfuncs_h_n.extractLynfamily,
				'Lypheon Machine Translation'                                   : pfuncs_h_n.extractLypheonMachineTranslation,
				'Machine Sliced Bread'                                          : pfuncs_h_n.extractMachineSlicedBread,
				'Madao Translations'                                            : pfuncs_h_n.extractMadaoTranslations,
				'MadoSpicy TL'                                                  : pfuncs_h_n.extractMadoSpicy,
				'Mahou Koukoku'                                                 : pfuncs_h_n.extractMahouKoukoku,
				'Mahoutsuki Translation'                                        : pfuncs_h_n.extractMahoutsuki,
				'Makina Translations'                                           : pfuncs_h_n.extractMakinaTranslations,
				'Mana Tank Magus'                                               : pfuncs_h_n.extractManaTankMagus,
				'Manga0205 Translations'                                        : pfuncs_h_n.extractManga0205Translations,
				'Maou na Anoko to murabito a'                                   : pfuncs_h_n.extractMaounaAnokotomurabitoa,
				'VaanCruze'                                                     : pfuncs_h_n.extractMaouTheYuusha,
				'Martial God Translator'                                        : pfuncs_h_n.extractMartialGodTranslator,
				'Mecha Mushroom Translations'                                   : pfuncs_h_n.extractMechaMushroom,
				'Yet Another Translation Site'                                  : pfuncs_h_n.extractMiaomix539,
				'Midnight Translation Blog'                                     : pfuncs_h_n.extractMidnightTranslationBlog,
				'Mike777ac'                                                     : pfuncs_h_n.extractMike777ac,
				'Mnemeaa'                                                       : pfuncs_h_n.extractMnemeaa,
				'Mojo Translations'                                             : pfuncs_h_n.extractMojoTranslations,
				"Monkoto's Translations"                                        : pfuncs_h_n.extractMonkotosTranslations,
				'Monk Translation'                                              : pfuncs_h_n.extractMonkTranslation,
				'Moon Bunny Cafe'                                               : pfuncs_h_n.extractMoonBunnyCafe,
				'Morrighan Sucks'                                               : pfuncs_h_n.extractMorrighanSucks,
				'Mousou Haven'                                                  : pfuncs_h_n.extractMousouHaven,
				'mousou-haven.com'                                              : pfuncs_h_n.extractMousouhaven,
				'MTLCrap'                                                       : pfuncs_h_n.extractMTLCrap,
				'My Purple World'                                               : pfuncs_h_n.extractMyPurpleWorld,
				'Mystique Translations'                                         : pfuncs_h_n.extractMystiqueTranslations,
				'Mythical Pagoda'                                               : pfuncs_h_n.extractMythicalPagoda,
				'N00b Translations'                                             : pfuncs_h_n.extractN00bTranslations,
				'Nakimushi'                                                     : pfuncs_h_n.extractNakimushi,
				'[nakulas]'                                                     : pfuncs_h_n.extractNakulas,
				'Nanjamora'                                                     : pfuncs_h_n.extractNanjamora,
				'(NanoDesu) - Amagi Brilliant Park '                            : pfuncs_h_n.extractNanoDesuAmagiBrilliantPark,
				'(NanoDesu) - Fate/Apocrypha'                                   : pfuncs_h_n.extractNanoDesuFateApocrypha,
				'(NanoDesu) - Fuyuu Gakuen no Alice and Shirley'                : pfuncs_h_n.extractNanoDesuFuyuuGakuennoAliceandShirley,
				'(NanoDesu) - Gekka no Utahime to Magi no Ou'                   : pfuncs_h_n.extractNanoDesuGekkanoUtahimetoMaginoOu,
				'(NanoDesu) - GJ-Bu'                                            : pfuncs_h_n.extractNanoDesuGJBu,
				'(NanoDesu) - Hai to Gensou no Grimgal'                         : pfuncs_h_n.extractNanoDesuHaitoGensounoGrimgal,
				'(NanoDesu) - Hentai Ouji to Warawanai Neko'                    : pfuncs_h_n.extractNanoDesuHentaiOujitoWarawanaiNeko,
				'(NanoDesu) - Kono Sekai ga Game Dato Ore Dake ga Shitteiru'   : pfuncs_h_n.extractNanoDesuKonoSekaigaGameDatoOreDakegaShitteiru,
				'(NanoDesu) - Kore wa Zombie Desu ka?'                          : pfuncs_h_n.extractNanoDesuKorewaZombieDesuka,
				'(NanoDesu) - Kurenai'                                          : pfuncs_h_n.extractNanoDesuKurenai,
				'NanoDesu Light Novel Translations'                             : pfuncs_h_n.extractNanoDesuLightNovelTranslations,
				'(NanoDesu) - Love★You'                                         : pfuncs_h_n.extractNanoDesuLoveYou,
				'(NanoDesu) - Maoyuu Maou Yuusha'                               : pfuncs_h_n.extractNanoDesuMaoyuuMaouYuusha,
				'(NanoDesu) - Mayo Chiki'                                       : pfuncs_h_n.extractNanoDesuMayoChiki,
				'(NanoDesu) - Ojamajo Doremi'                                   : pfuncs_h_n.extractNanoDesuOjamajoDoremi,
				'(NanoDesu) - Oreimo'                                           : pfuncs_h_n.extractNanoDesuOreimo,
				'(NanoDesu) - Rokka no Yuusha'                                  : pfuncs_h_n.extractNanoDesuRokkanoYuusha,
				'(NanoDesu) - Saenai Heroine no Sodatekata'                     : pfuncs_h_n.extractNanoDesuSaenaiHeroinenoSodatekata,
				'(NanoDesu) - Sasami-San@Ganbaranai'                            : pfuncs_h_n.extractNanoDesuSasamiSanGanbaranai,
				'(NanoDesu) - Seitokai no Ichizon'                              : pfuncs_h_n.extractNanoDesuSeitokainoIchizon,
				'(NanoDesu) - Sky World'                                        : pfuncs_h_n.extractNanoDesuSkyWorld,
				'(NanoDesu) - Yahari Ore no Seishun Love Come wa Machigatteiru' : pfuncs_h_n.extractNanoDesuYahariOrenoSeishunLoveComewaMachigatteiru,
				'Nanowave Translations'                                         : pfuncs_h_n.extractNanowaveTranslations,
				'National NEET'                                                 : pfuncs_h_n.extractNationalNEET,
				'Natsu TL'                                                      : pfuncs_h_n.extractNatsuTl,
				'Lazy NEET Translations'                                        : pfuncs_h_n.extractNEET,
				'NEET Translations'                                             : pfuncs_h_n.extractNeetTranslations,
				'Nega Translations'                                             : pfuncs_h_n.extractNegaTranslations,
				'Nekoyashiki'                                                   : pfuncs_h_n.extractNekoyashiki,
				'Neo Translations'                                              : pfuncs_h_n.extractNeoTranslations,
				'Nepustation'                                                   : pfuncs_h_n.extractNepustation,
				'Nightbreeze Translations'                                      : pfuncs_h_n.extractNightbreeze,
				'NightFall Translations'                                        : pfuncs_h_n.extractNightFallTranslations,
				'NinjaNUF'                                                      : pfuncs_h_n.extractNinjaNUF,
				'Nohohon Translation'                                           : pfuncs_h_n.extractNohohon,
				'Nooblate'                                                      : pfuncs_h_n.extractNooblate,
				'Noodletown Translated'                                         : pfuncs_h_n.extractNoodletownTranslated,
				'NOT Daily Translations'                                        : pfuncs_h_n.extractNotDailyTranslations,
				'NovelCow'                                                      : pfuncs_h_n.extractNovelCow,
				'Novelisation'                                                  : pfuncs_h_n.extractNovelisation,
				'Novel Saga'                                                    : pfuncs_h_n.extractNovelSaga,
				'Novels Ground'                                                 : pfuncs_h_n.extractNovelsGround,
				'Novels Japan'                                                  : pfuncs_h_n.extractNovelsJapan,
				'Novels Nao'                                                    : pfuncs_h_n.extractNovelsNao,
				'Novel Trans'                                                   : pfuncs_h_n.extractNovelTrans,
				'NoviceTranslator'                                              : pfuncs_h_n.extractNoviceTranslator,
				'Nowhere & Nothing'                                             : pfuncs_h_n.extractNowhereNothing,
				'NTRHolic'                                                      : pfuncs_h_n.extractNTRHolic,
				'Nutty is Procrastinating'                                      : pfuncs_h_n.extractNutty,
				'Ohanashimi'                                                    : pfuncs_o_u.extractOhanashimi,
				'OK Translation'                                                : pfuncs_o_u.extractOKTranslation,
				'Omega Harem'                                                   : pfuncs_o_u.extractOmegaHarem,
				'Omgitsaray Translations'                                       : pfuncs_o_u.extractOmgitsaray,
				'One Man Army Translations (OMA)'                               : pfuncs_o_u.extractOneManArmy,
				'One Man Army Translations'                                     : pfuncs_o_u.extractOneManArmy,
				'One Second Spring'                                             : pfuncs_o_u.extractOneSecondSpring,
				'お兄ちゃん、やめてぇ！'                                               : pfuncs_o_u.extractOniichanyamete,
				'Opinisaya.com'                                                 : pfuncs_o_u.extractOpinisaya,
				'Ore ga Heroine in English'                                     : pfuncs_o_u.extractOregaHeroineinEnglish,
				'Origin Novels'                                                 : pfuncs_o_u.extractOriginNovels,
				'Otome Revolution'                                              : pfuncs_o_u.extractOtomeRevolution,
				'otterspacetranslation'                                         : pfuncs_o_u.extractOtterspaceTranslation,
				'Outspan Foster'                                                : pfuncs_o_u.extractOutspanFoster,
				'Oyasumi Reads'                                                 : pfuncs_o_u.extractOyasumiReads,
				'Pact Web Serial'                                               : pfuncs_o_u.extractPactWebSerial,
				'pandafuqtranslations'                                          : pfuncs_o_u.extractPandafuqTranslations,
				"Pandora's Book"                                                : pfuncs_o_u.extractPandorasBook,
				'Patriarch Reliance'                                            : pfuncs_o_u.extractPatriarchReliance,
				'Paztok'                                                        : pfuncs_o_u.extractPaztok,
				'Pea\'s Kingdom'                                                : pfuncs_o_u.extractPeasKingdom,
				'Pea Translation'                                               : pfuncs_o_u.extractPeaTranslation,
				'Pekabo Blog'                                                   : pfuncs_o_u.extractPekaboBlog,
				'Penguin Overlord Translations'                                 : pfuncs_o_u.extractPenguinOverlordTranslations,
				'Pettanko Translations'                                         : pfuncs_o_u.extractPettankoTranslations,
				'Pielord Translations'                                          : pfuncs_o_u.extractPielordTranslations,
				'PiggyBottle Translations'                                      : pfuncs_o_u.extractPiggyBottleTranslations,
				'Pika Translations'                                             : pfuncs_o_u.extractPikaTranslations,
				'Pippi Site'                                                    : pfuncs_o_u.extractPippiSite,
				'A Place Of Legends'                                            : pfuncs_o_u.extractPlaceOfLegends,
				'PlainlyBored'                                                  : pfuncs_o_u.extractPlainlyBored,
				'Polyphonic Story Translation Group'                            : pfuncs_o_u.extractPolyphonicStoryTranslationGroup,
				'Popsiclete'                                                    : pfuncs_o_u.extractPopsiclete,
				'Premium Red Tea'                                               : pfuncs_o_u.extractPremiumRedTea,
				'Priddles Translations'                                         : pfuncs_o_u.extractPriddlesTranslations,
				'www.pridesfamiliarsmaidens.com'                                : pfuncs_o_u.extractPridesFamiliarsMaidens,
				'Pride X ReVamp'                                                : pfuncs_o_u.extractPrideXReVamp,
				'Prince Revolution!'                                            : pfuncs_o_u.extractPrinceRevolution,
				'ProcrasTranslation'                                            : pfuncs_o_u.extractProcrasTranslation,
				'Project Accelerator'                                           : pfuncs_o_u.extractProjectAccelerator,
				'Psicern.Translations'                                          : pfuncs_o_u.extractPsicernTranslations,
				'Pumpkin Translations'                                          : pfuncs_o_u.extractPumpkinTranslations,
				'putttytranslations'                                            : pfuncs_o_u.extractPuttty,
				'Qualidea of Scum and a Gold Coin'                              : pfuncs_o_u.extractQualideaofScumandaGoldCoin,
				'QualiTeaTranslations'                                          : pfuncs_o_u.extractQualiTeaTranslations,
				'Quality ★ Mistranslations'                                     : pfuncs_o_u.extractQualityMistranslations,
				'Radiant Translations'                                          : pfuncs_o_u.extractRadiantTranslations,
				'Rainbow Translations'                                          : pfuncs_o_u.extractRainbowTranslations,
				'Raising Angels & Defection'                                    : pfuncs_o_u.extractRaisingAngelsDefection,
				'Raising the Dead'                                              : pfuncs_o_u.extractRaisingTheDead,
				'RANCER'                                                        : pfuncs_o_u.extractRancer,
				'Rancer'                                                        : pfuncs_o_u.extractRancer,
				'Read Me Translations'                                          : pfuncs_o_u.extractReadMeTranslations,
				'Realm of Chaos'                                                : pfuncs_o_u.extractRealmOfChaos,
				'ℝeanとann@'                                                     : pfuncs_o_u.extractReantoAnna,
				'Rebirth Online World'                                          : pfuncs_o_u.extractRebirthOnlineWorld,
				'Rebirth Online'                                                : pfuncs_o_u.extractRebirthOnlineWorld,
				'Red Dragon Translations'                                       : pfuncs_o_u.extractRedDragonTranslations,
				'Reddy Creations'                                               : pfuncs_o_u.extractReddyCreations,
				'Red Lantern Archives'                                          : pfuncs_o_u.extractRedLanternArchives,
				'Reject Hero'                                                   : pfuncs_o_u.extractRejectHero,
				'Rhinabolla'                                                    : pfuncs_o_u.extractRhinabolla,
				'RidwanTrans'                                                   : pfuncs_o_u.extractRidwanTrans,
				'RinOtakuBlog'                                                  : pfuncs_o_u.extractRinOtakuBlog,
				'Rip translations'                                              : pfuncs_o_u.extractRiptranslations,
				'Rising Dragons Translation'                                    : pfuncs_o_u.extractRisingDragons,
				'Roasted Tea'                                                   : pfuncs_o_u.extractRoastedTea,
				'Romantic Dreamer\'s Sanctuary'                                 : pfuncs_o_u.extractRomanticDreamersSanctuary,
				'Root of Evil'                                                  : pfuncs_o_u.extractRootOfEvil,
				'Rosyfantasy - Always Dreaming'                                 : pfuncs_o_u.extractRosyFantasy,
				'Rosy Fantasy'                                                  : pfuncs_o_u.extractRosyFantasy,
				'Roxism HQ'                                                     : pfuncs_o_u.extractRoxism,
				"Rui's Translations"                                            : pfuncs_o_u.extractRuisTranslations,
				'Rumanshi\'s Lair'                                              : pfuncs_o_u.extractRumanshisLair,
				'Rumor\'s Block'                                                : pfuncs_o_u.extractRumorsBlock,
				'Ruze Translations'                                             : pfuncs_o_u.extractRuzeTranslations,
				'Saber Translations'                                            : pfuncs_o_u.extractSaberTranslations,
				'Saiaku Translations Blog'                                      : pfuncs_o_u.extractSaiakuTranslationsBlog,
				'桜翻訳! | Light novel translations'                             : pfuncs_o_u.extractSakurahonyaku,
				'Sandwich Kingdom'                                              : pfuncs_o_u.extractSandwichKingdom,
				'Sauri\'s TL Blog'                                              : pfuncs_o_u.extractSaurisTLBlog,
				'Scrya Translations'                                            : pfuncs_o_u.extractScryaTranslations,
				'SenjiQ creations'                                              : pfuncs_o_u.extractSenjiQcreations,
				'SETSUNA86BLOG'                                                 : pfuncs_o_u.extractSETSUNA86BLOG,
				'Shell2ly C-Novel Site'                                         : pfuncs_o_u.extractShell2lyCNovelSite,
				'Sherma Translations'                                           : pfuncs_o_u.extractShermaTranslations,
				'Shikkaku Translations'                                         : pfuncs_o_u.extractShikkakuTranslations,
				'Shin Sekai Yori – From the New World'                          : pfuncs_o_u.extractShinSekaiYori,
				'Shinsori Translations'                                         : pfuncs_o_u.extractShinsori,
				'Shin Translations'                                             : pfuncs_o_u.extractShinTranslations,
				'Shiroyukineko Translations'                                    : pfuncs_o_u.extractShiroyukineko,
				'Shokyuu Translations'                                          : pfuncs_o_u.extractShokyuuTranslations,
				'Silent Tl'                                                     : pfuncs_o_u.extractSilentTl,
				'Silva\'s Library'                                              : pfuncs_o_u.extractSilvasLibrary,
				'Silver Butterfly'                                              : pfuncs_o_u.extractSilverButterfly,
				'Sins of the Fathers'                                           : pfuncs_o_u.extractSinsOfTheFathers,
				'Skull Squadron'                                                : pfuncs_o_u.extractSkullSquadron,
				'Skythewood translations'                                       : pfuncs_o_u.extractSkythewood,
				'Sleepy Translations'                                           : pfuncs_o_u.extractSleepyTranslations,
				'Slime Lv1'                                                     : pfuncs_o_u.extractSlimeLv1,
				'-Sloth-'                                                       : pfuncs_o_u.extractSloth,
				'Sloth Translations Blog'                                       : pfuncs_o_u.extractSlothTranslationsBlog,
				'Snow & Dust'                                                   : pfuncs_o_u.extractSnowDust,
				'Snow Translations'                                             : pfuncs_o_u.extractSnowTranslations,
				'Snowy Publications'                                            : pfuncs_o_u.extractSnowyPublications,
				'Soaring Translations'                                          : pfuncs_o_u.extractSoaring,
				'Solitary Translation'                                          : pfuncs_o_u.extractSolitaryTranslation,
				'Solstar24'                                                     : pfuncs_o_u.extractSolstar24,
				'www.soltarination.org'                                         : pfuncs_o_u.extractSoltarination,
				'Soltarination Scanlations'                                     : pfuncs_o_u.extractSoltarinationScanlations,
				'Soojiki\'s Project'                                            : pfuncs_o_u.extractSoojikisProject,
				'Sora Translations'                                             : pfuncs_o_u.extractSoraTranslations,
				'Sora Translationsblog'                                         : pfuncs_o_u.extractSoraTranslations,
				'Supreme Origin Translations'                                   : pfuncs_o_u.extractSotranslations,
				'Sousetsuka'                                                    : pfuncs_o_u.extractSousetsuka,
				'Spiritual Transcription'                                       : pfuncs_o_u.extractSpiritualTranscription,
				'Spring Scents'                                                 : pfuncs_o_u.extractSpringScents,
				'Starrydawn Translations'                                       : pfuncs_o_u.extractStarrydawnTranslations,
				'Stellar Transformation Con.'                                   : pfuncs_o_u.extractStellarTransformationCon,
				'STL Translations'                                              : pfuncs_o_u.extractSTLTranslations,
				'Stone Burners'                                                 : pfuncs_o_u.extractStoneBurners,
				'Subudai11'                                                     : pfuncs_o_u.extractSubudai11,
				'Sun Shower Fields'                                             : pfuncs_o_u.extractSunShowerFields,
				'Super Potato Translations'                                     : pfuncs_o_u.extractSuperPotatoTranslations,
				'Suteki Da Ne'                                                  : pfuncs_o_u.extractSutekiDaNe,
				'Sweet A Collections'                                           : pfuncs_o_u.extractSweetACollections,
				'Sword and Game'                                                : pfuncs_o_u.extractSwordAndGame,
				'Sylver Translations'                                           : pfuncs_o_u.extractSylver,
				'Symbiote'                                                      : pfuncs_o_u.extractSymbiote,
				'~Taffy Translations~'                                          : pfuncs_o_u.extractTaffyTranslations,
				'Taida-dono Translations'                                       : pfuncs_o_u.extractTaidadonoTranslations,
				'Taint'                                                         : pfuncs_o_u.extractTaint,
				'Tales of MU'                                                   : pfuncs_o_u.extractTalesOfMU,
				'The Tales of Paul Twister'                                     : pfuncs_o_u.extractTalesOfPaulTwister,
				'Tales of The Forgottenslayer'                                  : pfuncs_o_u.extractTalesofTheForgottenslayer,
				'tap-trans » tappity tappity tap.'                              : pfuncs_o_u.extractTaptrans,
				'Tarable Translations'                                          : pfuncs_o_u.extractTarableTranslations,
				'Tatakau Shisho Light Novel Translation'                        : pfuncs_o_u.extractTatakauShishoLightNovelTranslation,
				'Tensai Translations'                                           : pfuncs_o_u.extractTensaiTranslations,
				'Tentatively under construction'                                : pfuncs_o_u.extractTentativelyUnderconstruction,
				'Ten Thousand Heaven Controlling Sword'                         : pfuncs_o_u.extractTenThousandHeavenControllingSword,
				'Terminus Translation'                                          : pfuncs_o_u.extractTerminusTranslation,
				'ThatGuyOverThere'                                              : pfuncs_o_u.extractThatGuyOverThere,
				'The Asian Cult'                                                : pfuncs_o_u.extractTheAsianCult,
				'The Beginning After The End Novel'                             : pfuncs_o_u.extractTheBeginningAfterTheEnd,
				'TheDefend Translations'                                        : pfuncs_o_u.extractTheDefendTranslations,
				'The Iron Teeth'                                                : pfuncs_o_u.extractTheIronTeeth,
				'The Last Skull'                                                : pfuncs_o_u.extractTheLastSkull,
				'TheLazy9'                                                      : pfuncs_o_u.extractTheLazy9,
				'The Mustang Translator'                                        : pfuncs_o_u.extractTheMustangTranslator,
				'The Named'                                                     : pfuncs_o_u.extractTheNamed,
				'The Sphere'                                                    : pfuncs_o_u.extractTheSphere,
				'This World Work'                                               : pfuncs_o_u.extractThisWorldWork,
				'Thunder Translation'                                           : pfuncs_o_u.extractThunder,
				'Thyaeria Translations'                                         : pfuncs_o_u.extractThyaeria,
				'Tieshaunn'                                                     : pfuncs_o_u.extractTieshaunn,
				'Tinkerbell-san'                                                : pfuncs_o_u.extractTinkerbellsan,
				'TL Syosetsu'                                                   : pfuncs_o_u.extractTLSyosetsu,
				'Tofubyu'                                                       : pfuncs_o_u.extractTofubyu,
				'Tomorolls'                                                     : pfuncs_o_u.extractTomorolls,
				'Tony Yon Ka'                                                   : pfuncs_o_u.extractTonyYonKa,
				'Totally Insane Tranlation'                                     : pfuncs_o_u.extractTotallyInsaneTranslation,
				'Totally Insane Translation'                                    : pfuncs_o_u.extractTotallyInsaneTranslation,
				'Totokk\'s Translations'                                        : pfuncs_o_u.extractTotokk,
				'Towards the Sky~'                                              : pfuncs_o_u.extractTowardsTheSky,
				'Translating For Your Pleasure'                                 : pfuncs_o_u.extractTranslatingForYourPleasure,
				'Translating Ze Tian Ji'                                        : pfuncs_o_u.extractTranslatingZeTianJi,
				'Translation Nations'                                           : pfuncs_o_u.extractTranslationNations,
				'Translation Raven'                                             : pfuncs_o_u.extractTranslationRaven,
				'Translations From Outer Space'                                 : pfuncs_o_u.extractTranslationsFromOuterSpace,
				'Translation Treasure Box'                                      : pfuncs_o_u.extractTranslationTreasureBox,
				'Trinity Archive'                                               : pfuncs_o_u.extractTrinityArchive,
				'Tripp Translations'                                            : pfuncs_o_u.extractTrippTl,
				'Trung Nguyen'                                                  : pfuncs_o_u.extractTrungNguyen,
				'Trungt Nguyen 123'                                             : pfuncs_o_u.extractTrungtNguyen,
				'Try Translations'                                              : pfuncs_o_u.extractTryTranslations,
				'Tseirp Translations'                                           : pfuncs_o_u.extractTseirpTranslations,
				'Tsuigeki Translations'                                         : pfuncs_o_u.extractTsuigeki,
				'Tsukigomori'                                                   : pfuncs_o_u.extractTsukigomori,
				'Tumble Into Fantasy'                                           : pfuncs_o_u.extractTumbleIntoFantasy,
				'Turb0 Translation'                                             : pfuncs_o_u.extractTurb0,
				'Turtle and Hare Translations'                                  : pfuncs_o_u.extractTurtleandHareTranslations,
				'中翻英圖書館 Translations'                                       : pfuncs_o_u.extractTuShuGuan,
				'Tus-Trans'                                                     : pfuncs_o_u.extractTusTrans,
				'Twelve Months of May'                                          : pfuncs_o_u.extractTwelveMonthsofMay,
				'Twig'                                                          : pfuncs_o_u.extractTwig,
				'Twisted Cogs'                                                  : pfuncs_o_u.extractTwistedCogs,
				'Tyrant\'s Eye Translations'                                    : pfuncs_o_u.extractTyrantsEyeTranslations,
				'「\u3000」'                                                      : pfuncs_o_u.extractU3000,
				'U Donate We Translate'                                         : pfuncs_o_u.extractUDonateWeTranslate,
				'Ukel2x'                                                        : pfuncs_o_u.extractUkel2x,
				'Ultimate Arcane'                                               : pfuncs_o_u.extractUltimateArcane,
				'Unchained Translation'                                         : pfuncs_o_u.extractUnchainedTranslation,
				'Undecent Translations'                                         : pfuncs_o_u.extractUndecentTranslations,
				'Universes With Meaning'                                        : pfuncs_o_u.extractUniversesWithMeaning,
				'Unlimited Novel Failures'                                      : pfuncs_o_u.extractUnlimitedNovelFailures,
				'Unlimited Story Works'                                         : pfuncs_o_u.extractUnlimitedStoryWorks,
				'unnamedtranslations.blogspot.com'                              : pfuncs_o_u.extractUnnamedtranslations,
				'Untuned Translation Blog'                                      : pfuncs_o_u.extractUntunedTranslation,
				'Useless no 4'                                                  : pfuncs_o_u.extractUselessno4,
				'Verathragana Stories'                                          : pfuncs_v_other.extractVerathragana,
				'Village Translations'                                          : pfuncs_v_other.extractVillageTranslations,
				'Void Translations'                                             : pfuncs_v_other.extractVoidTranslations,
				'Volare Translations'                                           : pfuncs_v_other.extractVolareTranslations,
				'Walking the Storm'                                             : pfuncs_v_other.extractWalkingTheStorm,
				'Walk the Jiang Hu'                                             : pfuncs_v_other.extractWalkTheJiangHu,
				'Wat Da Meow'                                                   : pfuncs_v_other.extractWatDaMeow,
				'Watermelon Helmets'                                            : pfuncs_v_other.extractWatermelonHelmets,
				'World of Watermelons'                                          : pfuncs_v_other.extractWatermelons,
				'WCC Translation'                                               : pfuncs_v_other.extractWCCTranslation,
				'Weaving stories and building castles in the clouds'            : pfuncs_v_other.extractWeavingstoriesandbuildingcastlesintheclouds,
				'Web Novel Japanese Translation'                                : pfuncs_v_other.extractWebNovelJapaneseTranslation,
				'Welcome To The Underdark'                                      : pfuncs_v_other.extractWelcomeToTheUnderdark,
				'Wele Translation'                                              : pfuncs_v_other.extractWeleTranslation,
				'When The Hunting Party Came'                                   : pfuncs_v_other.extractWhenTheHuntingPartyCame,
				'Whimsical Land'                                                : pfuncs_v_other.extractWhimsicalLand,
				'White Tiger Translations'                                      : pfuncs_v_other.extractWhiteTigerTranslations,
				'Willful Casual'                                                : pfuncs_v_other.extractWillfulCasual,
				'Witch Life Novel'                                              : pfuncs_v_other.extractWitchLife,
				"WizThief's Novels"                                             : pfuncs_v_other.extractWizThiefsNovels,
				'WL Translations'                                               : pfuncs_v_other.extractWLTranslations,
				'Wolfie Translation'                                            : pfuncs_v_other.extractWolfieTranslation,
				'Word of Craft'                                                 : pfuncs_v_other.extractWordofCraft,
				'World of Summie'                                               : pfuncs_v_other.extractWorldofSummie,
				'Worm - A Complete Web Serial'                                  : pfuncs_v_other.extractWormACompleteWebSerial,
				'Wuxia Heroes'                                                  : pfuncs_v_other.extractWuxiaHeroes,
				'WuxiaSociety'                                                  : pfuncs_v_other.extractWuxiaSociety,
				'Wuxia Translations'                                            : pfuncs_v_other.extractWuxiaTranslations,
				'Wuxia Translators'                                             : pfuncs_v_other.extractWuxiaTranslators,
				'Wuxiaworld'                                                    : pfuncs_v_other.extractWuxiaworld,
				'Wuxiwish'                                                      : pfuncs_v_other.extractWuxiwish,
				'Xant & Minions'                                                : pfuncs_v_other.extractXantAndMinions,
				'xantbos.wordpress.com'                                         : pfuncs_v_other.extractXantbos,
				'Xant Does Stuff and Things'                                    : pfuncs_v_other.extractXantDoesStuffAndThings,
				'XCrossJ'                                                       : pfuncs_v_other.extractXCrossJ,
				"Xiaowen206's Blog"                                             : pfuncs_v_other.extractXiaowen206sBlog,
				'Yi Yue Translation'                                            : pfuncs_v_other.extractYiYueTranslation,
				'Yoraikun Translation'                                          : pfuncs_v_other.extractYoraikun,
				'Youjinsite Translations'                                       : pfuncs_v_other.extractYoujinsite,
				'Youko Advent'                                                  : pfuncs_v_other.extractYoukoAdvent,
				'Youshoku Translations'                                         : pfuncs_v_other.extractYoushoku,
				'youtsubasilver\'s Blog'                                        : pfuncs_v_other.extractYoutsubasilversBlog,
				'Yukkuri Free Time Literature Service'                          : pfuncs_v_other.extractYukkuri,
				'Zen Translations'                                              : pfuncs_v_other.extractZenTranslations,
				'Zeonic'                                                        : pfuncs_v_other.extractZeonic,
				'Ziru\'s Musings | Translations~'                               : pfuncs_v_other.extractZiruTranslations,
				'The Zombie Knight'                                             : pfuncs_v_other.extractZombieKnight,
				'ZSW'                                                           : pfuncs_v_other.extractZSW,
				"Zxzxzx's blog"                                                 : pfuncs_v_other.extractZxzxzxsBlog,
				'一期一会, 万歳!'                                                 : pfuncs_v_other.extract一期一会万歳,
				'天才創造すなわち百合'                                               : pfuncs_v_other.extract天才創造すなわち百合,
				'睡眠中毒'                                                        : pfuncs_v_other.extract睡眠中毒,
				'輝く世界'                                                        : pfuncs_v_other.extract輝く世界,
				'12 Superlatives'                                               : pfuncs_v_other.extract12Superlatives,
				'1HP'                                                           : pfuncs_v_other.extract1HP,
				'77 Novel'                                                      : pfuncs_v_other.extract77Novel,
				'7 Days Trial'                                                  : pfuncs_v_other.extract7DaysTrial,
				'87 Percent Translation'                                        : pfuncs_v_other.extract87Percent,



				# Broken
				'Require: Cookie'                                               : pfuncs_stub.extractNop,


				'Blue Phoenix'                                                  : pfuncs_a_g.extractBluePhoenix,
				'Demon Translations'                                            : pfuncs_a_g.extractDemonTranslations,
				'Fantasy novels'                                                : pfuncs_a_g.extractFantasyNovels,
				'HalfElementMaster Translation'                                 : pfuncs_h_n.extractHalfElementMasterTranslation,
				'Love me if you dare'                                           : pfuncs_h_n.extractLoveMeIfYouDare,
				'Mineral Water Translation'                                     : pfuncs_h_n.extractMineralWaterTranslation,
				'Rinkage Translation'                                           : pfuncs_o_u.extractRinkageTranslation,
				'Selkin Novel'                                                  : pfuncs_o_u.extractSelkinNovel,
				'Shikkaku Translations'                                         : pfuncs_o_u.extractShikkakuTranslations,
				'Startling Surprises at Every Step'                             : pfuncs_o_u.extractStartlingSurprisesAtEveryStep,
				'Wish Upon A Hope'                                              : pfuncs_v_other.extractWishUponAHope,


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
				print("Missed:")
				print("	Source: '%s'" % (item['srcname'], ))
				print("	Title:  '%s'" % (item['title'], ))
				print("	Tags:   '%s'" % (item['tags'], ))
				print("	Vol %s, chp %s, fragment %s, postfix '%s'" % (vol, chp, frag, postfix))
				# print("Missed: '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))
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

	# Manual patches for dealing with a few broken feeds.
	def checkIgnore(self, feedDat):

		# Japtem seems to put their comments in their main feed, for no good reason.
		if feedDat['srcname'] == "Japtem" and feedDat['title'].startswith("By: "):
			return True
		if feedDat['srcname'] == "Zeonic" and feedDat['title'].startswith("By: "):
			return True
		if feedDat['srcname'] == 'Sora Translations' and feedDat['title'].startswith("Comment on"):
			return True


		return False

	def processFeedData(self, feedDat, tx_raw=True, tx_parse=True):

		if any([item in feedDat['linkUrl'] for item in skip_filter]):
			print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return


		netloc = urllib.parse.urlparse(feedDat['linkUrl']).netloc

		nicename = feedNameLut.getNiceName(feedDat['linkUrl'])
		if not nicename:
			nicename = netloc
		feedDat['srcname'] = nicename

		if self.checkIgnore(feedDat):
			return

		# print("ProcessFeedData! ", netloc)

		# A bunch of crap is aggregated through the "feedproxy.google.com" netloc.
		if not WebMirror.rules.netloc_send_feed(netloc) and not "feedproxy.google.com" in netloc:
			print("Not sending data for netloc: ", netloc)
			return

		new = self.getProcessedReleaseInfo(feedDat)

		if tx_parse:
			if new:
				self.amqp_put_item(new)


		raw = self.getRawFeedMessage(feedDat)
		if tx_raw:
			if raw:
				self.amqp_put_item(raw)
