
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

				"Hold 'X' and Click"                                            : pfuncs.extractHoldX,
				"Pea's Kingdom"                                                 : pfuncs.extractPeasKingdom,
				'1HP'                                                           : pfuncs.extract1HP,
				'87 Percent Translation'                                        : pfuncs.extract87Percent,
				'A fish once said this to me'                                   : pfuncs.extractDarkFish,
				'A Place Of Legends'                                            : pfuncs.extractPlaceOfLegends,
				'A0132'                                                         : pfuncs.extractA0132,
				'AFlappyTeddyBird'                                              : pfuncs.extractAFlappyTeddyBird,
				'Alcsel Translations'                                           : pfuncs.extractAlcsel,
				'Alyschu & Co'                                                  : pfuncs.extractAlyschuCo,
				'Anathema Serial'                                               : pfuncs.extractAnathema,
				'Andrew9495\'s MTL corner'                                      : pfuncs.extractAndrew9495,
				'Aquarilas\' Scenario'                                          : pfuncs.extractAquarilasScenario,
				'Ark Machine Translations'                                      : pfuncs.extractArkMachineTranslations,
				'AsherahBlue\'s Notebook'                                       : pfuncs.extractAsherahBlue,
				'Aten Translations'                                             : pfuncs.extractAtenTranslations,
				'Avert Translations'                                            : pfuncs.extractAvert,
				'Azure Sky Translation'                                         : pfuncs.extractAzureSky,
				'Azurro 4 Cielo'                                                : pfuncs.extractAzurro,
				'Baka Dogeza Translation'                                       : pfuncs.extractBakaDogeza,
				'Bcat00 Translation'                                            : pfuncs.extractBcat00,
				'Beehugger'                                                     : pfuncs.extractBeehugger,
				'Berseker Translations'                                         : pfuncs.extractBersekerTranslations,
				'Binggo&Corp'                                                   : pfuncs.extractBinggoCorp,
				'Binhjamin'                                                     : pfuncs.extractBinhjamin,
				'Blue Silver Translations'                                      : pfuncs.extractBlueSilverTranslations,
				'Bu Bu Jing Xin Translation'                                    : pfuncs.extractBuBuJingXinTrans,
				'Burei Dan Works'                                               : pfuncs.extractBureiDan,
				'C.E. Light Novel Translations'                                 : pfuncs.extractCeLn,
				'Calico x Tabby'                                                : pfuncs.extractCalicoxTabby,
				'Cas Project Site'                                              : pfuncs.extractCasProjectSite,
				'Ceruleonice Translations'                                      : pfuncs.extractCeruleonice,
				'Chinese BL Translations'                                       : pfuncs.extractChineseBLTranslations,
				'Circus Translations'                                           : pfuncs.extractCircusTranslations,
				'Clicky Click Translation'                                      : pfuncs.extractClicky,
				'Clover\'s Nook'                                                : pfuncs.extractCloversNook,
				'CookiePasta'                                                   : pfuncs.extractCookiePasta,
				'CrystalRainDescends'                                           : pfuncs.extractCrystalRainDescends,
				'CtrlAlcalá'                                                    : pfuncs.extractCtrlAlcala,
				'Dao Seeker Blog'                                               : pfuncs.extractDaoSeekerBlog,
				'Dawning Howls'                                                 : pfuncs.extractDawningHowls,
				'Defiring'                                                      : pfuncs.extractDefiring,
				'Dewey Night Unrolls'                                           : pfuncs.extractDeweyNightUnrolls,
				'Distracted Translations'                                       : pfuncs.extractDistractedTranslations,
				'Diwasteman'                                                    : pfuncs.extractDiwasteman,
				'DragomirCM'                                                    : pfuncs.extractDragomirCM,
				'Dreadful Decoding'                                             : pfuncs.extractDreadfulDecoding,
				'Dreams of Jianghu'                                             : pfuncs.extractDreamsOfJianghu,
				'Dynamis Gaul Light Novel'                                      : pfuncs.extractDynamisGaul,
				'End Online Novel'                                              : pfuncs.extractEndOnline,
				'Ensj Translations'                                             : pfuncs.extractEnsjTranslations,
				'EnTruce Translations'                                          : pfuncs.extractEnTruceTranslations,
				'Ero Light Novel Translations'                                  : pfuncs.extractEroLightNovelTranslations,
				'Eros Workshop'                                                 : pfuncs.extractErosWorkshop,
				'Fanatical'                                                     : pfuncs.extractFanatical,
				'FeedProxy'                                                     : pfuncs.extractFeedProxy,
				'Firebird\'s Nest'                                              : pfuncs.extractFirebirdsNest,
				'Five Star Specialists'                                         : pfuncs.extractFiveStar,
				'Flower Bridge Too'                                             : pfuncs.extractFlowerBridgeToo,
				'Forgetful Dreamer'                                             : pfuncs.extractForgetfulDreamer,
				'Forgotten Conqueror'                                           : pfuncs.extractForgottenConqueror,
				'Frostfire 10'                                                  : pfuncs.extractFrostfire10,
				'Fudge Translations'                                            : pfuncs.extractFudgeTranslations,
				'Gila Translation Monster'                                      : pfuncs.extractGilaTranslation,
				'Giraffe Corps'                                                 : pfuncs.extractGiraffe,
				'Goddess! Grant Me a Girlfriend!!'                              : pfuncs.extractGoddessGrantMeaGirlfriend,
				'Gravity Tales'                                                 : pfuncs.extractGravityTranslation,
				'guhehe.TRANSLATIONS'                                           : pfuncs.extractGuhehe,
				'Guro Translation'                                              : pfuncs.extractGuroTranslation,
				'Hajiko translation'                                            : pfuncs.extractHajiko,
				'HaruPARTY'                                                     : pfuncs.extractHaruPARTY,
				'Henouji Translation'                                           : pfuncs.extractHenoujiTranslation,
				'Hokage Translations'                                           : pfuncs.extractHokageTrans,
				'Hot Cocoa Translations'                                        : pfuncs.extractHotCocoa,
				'Imoutolicious Light Novel Translations'                        : pfuncs.extractImoutolicious,
				'Infinite Novel Translations'                                   : pfuncs.extractInfiniteNovelTranslations,
				'Isekai Mahou Translations!'                                    : pfuncs.extractIsekaiMahou,
				'Isekai Soul-Cyborg Translations'                               : pfuncs.extractIsekaiTranslation,
				'Iterations within a Thought-Eclipse'                           : pfuncs.extractIterations,
				'izra709 | B Group no Shounen Translations'                     : pfuncs.extractIzra709,
				'Japtem'                                                        : pfuncs.extractJaptem,
				'JawzTranslations'                                              : pfuncs.extractJawzTranslations,
				'Joeglen\'s Translation Space'                                  : pfuncs.extractJoeglensTranslationSpace,
				'Kaezar Translations'                                           : pfuncs.extractKaezar,
				'Kahoim Translations'                                           : pfuncs.extractKahoim,
				'Kami Translation'                                              : pfuncs.extractKamiTranslation,
				'Kerambit\'s Incisions'                                         : pfuncs.extractKerambit,
				'King Jaahn\'s Subjects'                                        : pfuncs.extractKingJaahn,
				'Kiri Leaves'                                                   : pfuncs.extractKiri,
				'KobatoChanDaiSukiScan'                                         : pfuncs.extractKobatoChanDaiSukiScan,
				'Konobuta'                                                      : pfuncs.extractKonobuta,
				'Kore Yori Hachidori'                                           : pfuncs.extractKoreYoriHachidori,
				'Korean Novel Translations'                                     : pfuncs.extractKoreanNovelTrans,
				'Kyakka'                                                        : pfuncs.extractKyakka,
				'Larvyde'                                                       : pfuncs.extractLarvyde,
				'Lascivious Imouto'                                             : pfuncs.extractLasciviousImouto,
				'Lazy NEET Translations'                                        : pfuncs.extractNEET,
				'Legend of Galactic Heroes Translation Project'                 : pfuncs.extractLegendofGalacticHeroes,
				'Lingson\'s Translations'                                       : pfuncs.extractLingson,
				'Ln Addiction'                                                  : pfuncs.extractLnAddiction,
				'Loiterous'                                                     : pfuncs.extractLoiterous,
				'Lonahora'                                                      : pfuncs.extractLonahora,
				'Lost in Translation'                                           : pfuncs.extractLostInTranslation,
				'Lunaris'                                                       : pfuncs.extractLunaris,
				'Lunate'                                                        : pfuncs.extractLunate,
				'LygarTranslations'                                             : pfuncs.extractLygarTranslations,
				'Lylis Translations'                                            : pfuncs.extractLylisTranslations,
				'Machine Sliced Bread'                                          : pfuncs.extractMachineSlicedBread,
				'Madao Translations'                                            : pfuncs.extractMadaoTranslations,
				'MadoSpicy TL'                                                  : pfuncs.extractMadoSpicy,
				'Mahou Koukoku'                                                 : pfuncs.extractMahouKoukoku,
				'Mahoutsuki Translation'                                        : pfuncs.extractMahoutsuki,
				'Makina Translations'                                           : pfuncs.extractMakinaTranslations,
				'Mana Tank Magus'                                               : pfuncs.extractManaTankMagus,
				'Manga0205 Translations'                                        : pfuncs.extractManga0205Translations,
				'Mecha Mushroom Translations'                                   : pfuncs.extractMechaMushroom,
				'Mike777ac'                                                     : pfuncs.extractMike777ac,
				'Monk Translation'                                              : pfuncs.extractMonkTranslation,
				'Moon Bunny Cafe'                                               : pfuncs.extractMoonBunnyCafe,
				'Morrighan Sucks'                                               : pfuncs.extractMorrighanSucks,
				'Nanjamora'                                                     : pfuncs.extractNanjamora,
				'Natsu TL'                                                      : pfuncs.extractNatsuTl,
				'NEET Translations'                                             : pfuncs.extractNeetTranslations,
				'Nekoyashiki'                                                   : pfuncs.extractNekoyashiki,
				'Neo Translations'                                              : pfuncs.extractNeoTranslations,
				'Nightbreeze Translations'                                      : pfuncs.extractNightbreeze,
				'Nohohon Translation'                                           : pfuncs.extractNohohon,
				'Nooblate'                                                      : pfuncs.extractNooblate,
				'Novels Nao'                                                    : pfuncs.extractNovelsNao,
				'NoviceTranslator'                                              : pfuncs.extractNoviceTranslator,
				'Nutty is Procrastinating'                                      : pfuncs.extractNutty,
				'Ohanashimi'                                                    : pfuncs.extractOhanashimi,
				'OK Translation'                                                : pfuncs.extractOKTranslation,
				'Omega Harem'                                                   : pfuncs.extractOmegaHarem,
				'Omgitsaray Translations'                                       : pfuncs.extractOmgitsaray,
				'One Man Army Translations (OMA)'                               : pfuncs.extractOneManArmy,
				'One Man Army Translations'                                     : pfuncs.extractOneManArmy,
				'One Second Spring'                                             : pfuncs.extractOneSecondSpring,
				'Origin Novels'                                                 : pfuncs.extractOriginNovels,
				'otterspacetranslation'                                         : pfuncs.extractOtterspaceTranslation,
				'Outspan Foster'                                                : pfuncs.extractOutspanFoster,
				'Pika Translations'                                             : pfuncs.extractPikaTranslations,
				'PlainlyBored'                                                  : pfuncs.extractPlainlyBored,
				'Prince Revolution!'                                            : pfuncs.extractPrinceRevolution,
				'putttytranslations'                                            : pfuncs.extractPuttty,
				'Radiant Translations'                                          : pfuncs.extractRadiantTranslations,
				'Rainbow Translations'                                          : pfuncs.extractRainbowTranslations,
				'Raising the Dead'                                              : pfuncs.extractRaisingTheDead,
				'RANCER'                                                        : pfuncs.extractRancer,
				'Rebirth Online World'                                          : pfuncs.extractRebirthOnlineWorld,
				'Rebirth Online'                                                : pfuncs.extractRebirthOnlineWorld,
				'Red Dragon Translations'                                       : pfuncs.extractRedDragonTranslations,
				'Reddy Creations'                                               : pfuncs.extractReddyCreations,
				'Reigokai: Isekai Translations'                                 : pfuncs.extractIsekaiTranslations,
				'Require: Cookie'                                               : pfuncs.extractRequireCookie,
				'Rhinabolla'                                                    : pfuncs.extractRhinabolla,
				'Rising Dragons Translation'                                    : pfuncs.extractRisingDragons,
				'Roxism HQ'                                                     : pfuncs.extractRoxism,
				'Rumor\'s Block'                                                : pfuncs.extractRumorsBlock,
				'Ruze Translations'                                             : pfuncs.extractRuzeTranslations,
				'Scrya Translations'                                            : pfuncs.extractScryaTranslations,
				'Shikkaku Translations'                                         : pfuncs.extractShikkakuTranslations,
				'Shin Sekai Yori – From the New World'                          : pfuncs.extractShinSekaiYori,
				'Shin Translations'                                             : pfuncs.extractShinTranslations,
				'Shinsori Translations'                                         : pfuncs.extractShinsori,
				'Shiroyukineko Translations'                                    : pfuncs.extractShiroyukineko,
				'Silent Tl'                                                     : pfuncs.extractSilentTl,
				'Silva\'s Library'                                              : pfuncs.extractSilvasLibrary,
				'Sins of the Fathers'                                           : pfuncs.extractSinsOfTheFathers,
				'Skythewood translations'                                       : pfuncs.extractSkythewood,
				'Soaring Translations'                                          : pfuncs.extractSoaring,
				'Solitary Translation'                                          : pfuncs.extractSolitaryTranslation,
				'Soojiki\'s Project'                                            : pfuncs.extractSoojikisProject,
				'Sora Translationsblog'                                         : pfuncs.extractSoraTranslations,
				'Sousetsuka'                                                    : pfuncs.extractSousetsuka,
				'Subudai11'                                                     : pfuncs.extractSubudai11,
				'Supreme Origin Translations'                                   : pfuncs.extractSotranslations,
				'Suteki Da Ne'                                                  : pfuncs.extractSutekiDaNe,
				'Sword and Game'                                                : pfuncs.extractSwordAndGame,
				'Sylver Translations'                                           : pfuncs.extractSylver,
				'Tales of MU'                                                   : pfuncs.extractTalesOfMU,
				'Tensai Translations'                                           : pfuncs.extractTensaiTranslations,
				'ThatGuyOverThere'                                              : pfuncs.extractThatGuyOverThere,
				'The Beginning After The End'                                   : pfuncs.extractBeginningAfterTheEnd,
				'The C-Novel Project'                                           : pfuncs.extractCNovelProj,
				'The Mustang Translator'                                        : pfuncs.extractTheMustangTranslator,
				'The Tales of Paul Twister'                                     : pfuncs.extractTalesOfPaulTwister,
				'The Zombie Knight'                                             : pfuncs.extractZombieKnight,
				'TheLazy9'                                                      : pfuncs.extractTheLazy9,
				'Thunder Translation'                                           : pfuncs.extractThunder,
				'Thyaeria Translations'                                         : pfuncs.extractThyaeria,
				'Tomorolls'                                                     : pfuncs.extractTomorolls,
				'Tony Yon Ka'                                                   : pfuncs.extractTonyYonKa,
				'Totally Insane Tranlation'                                     : pfuncs.extractTotallyInsaneTranslation,
				'Totally Insane Translation'                                    : pfuncs.extractTotallyInsaneTranslation,
				'Totokk\'s Translations'                                        : pfuncs.extractTotokk,
				'Translated by a Clown'                                         : pfuncs.extractClownTrans,
				'Translating Ze Tian Ji'                                        : pfuncs.extractTranslatingZeTianJi,
				'Translation Nations'                                           : pfuncs.extractTranslationNations,
				'Translation Raven'                                             : pfuncs.extractTranslationRaven,
				'Tripp Translations'                                            : pfuncs.extractTrippTl,
				'Trungt Nguyen 123'                                             : pfuncs.extractTrungtNguyen,
				'Tsuigeki Translations'                                         : pfuncs.extractTsuigeki,
				'Tsukigomori'                                                   : pfuncs.extractTsukigomori,
				'Turb0 Translation'                                             : pfuncs.extractTurb0,
				'Twisted Cogs'                                                  : pfuncs.extractTwistedCogs,
				'Ultimate Arcane'                                               : pfuncs.extractUltimateArcane,
				'Unchained Translation'                                         : pfuncs.extractUnchainedTranslation,
				'Untuned Translation Blog'                                      : pfuncs.extractUntunedTranslation,
				'VaanCruze'                                                     : pfuncs.extractMaouTheYuusha,
				'Verathragana Stories'                                          : pfuncs.extractVerathragana,
				'Void Translations'                                             : pfuncs.extractVoidTranslations,
				'Walking the Storm'                                             : pfuncs.extractWalkingTheStorm,
				'Wat Da Meow'                                                   : pfuncs.extractWatDaMeow,
				'WCC Translation'                                               : pfuncs.extractWCCTranslation,
				'Web Novel Japanese Translation'                                : pfuncs.extractWebNovelJapaneseTranslation,
				'Witch Life Novel'                                              : pfuncs.extractWitchLife,
				'Wolfie Translation'                                            : pfuncs.extractWolfieTranslation,
				'World of Watermelons'                                          : pfuncs.extractWatermelons,
				'Wuxia Heroes'                                                  : pfuncs.extractWuxiaHeroes,
				'Wuxia Translations'                                            : pfuncs.extractWuxiaTranslations,
				'WuxiaSociety'                                                  : pfuncs.extractWuxiaSociety,
				'Wuxiaworld'                                                    : pfuncs.extractWuxiaworld,
				'Xant & Minions'                                                : pfuncs.extractXantAndMinions,
				'Yoraikun Translation'                                          : pfuncs.extractYoraikun,
				'Youjinsite Translations'                                       : pfuncs.extractYoujinsite,
				'Youshoku Translations'                                         : pfuncs.extractYoushoku,
				'Yukkuri Free Time Literature Service'                          : pfuncs.extractYukkuri,
				'Ziru\'s Musings | Translations~'                               : pfuncs.extractZiruTranslations,
				'ZSW'                                                           : pfuncs.extractZSW,
				'~Taffy Translations~'                                          : pfuncs.extractTaffyTranslations,
				'ℝeanとann@'                                                     : pfuncs.extractReantoAnna,
				'お兄ちゃん、やめてぇ！'                                               : pfuncs.extractOniichanyamete,
				'中翻英圖書館 Translations'                                       : pfuncs.extractTuShuGuan,
				'桜翻訳! | Light novel translations'                             : pfuncs.extractSakurahonyaku,
				'Pippi Site'                                                    : pfuncs.extractPippiSite,
				'Helidwarf'                                                     : pfuncs.extractHelidwarf,

				'Walk the Jiang Hu'                                             : pfuncs.extractWalkTheJiangHu,
				'Universes With Meaning'                                        : pfuncs.extractUniversesWithMeaning,


				# KnW mess
				'Blazing Translations'                                          : pfuncs.extractKnW,
				'CapsUsingShift Tl'                                             : pfuncs.extractKnW,
				'Insignia Pierce'                                               : pfuncs.extractKnW,
				'Kiriko Translations'                                           : pfuncs.extractKnW,
				'Konjiki no Wordmaster'                                         : pfuncs.extractKnW,
				'Loliquent'                                                     : pfuncs.extractKnW,
				'Pummels Translations'                                          : pfuncs.extractKnW,
				'XCrossJ'                                                       : pfuncs.extractKnW,


				'Ducky\'s English Translations'                                 : pfuncs.extractBase,
				'Dark Translations'                                             : pfuncs.extractBase,
				'Bad Translation'                                               : pfuncs.extractBase,
				'LordofScrubs'                                                  : pfuncs.extractBase,
				'Roasted Tea'                                                   : pfuncs.extractBase,
				'Undecent Translations'                                         : pfuncs.extractBase,
				'pandafuqtranslations'                                          : pfuncs.extractBase,

				'(NanoDesu) - Amagi Brilliant Park '                            : pfuncs.extractBase,
				'(NanoDesu) - Fate/Apocrypha'                                   : pfuncs.extractBase,
				'(NanoDesu) - Fuyuu Gakuen no Alice and Shirley'                : pfuncs.extractBase,
				'(NanoDesu) - Gekka no Utahime to Magi no Ou'                   : pfuncs.extractBase,
				'(NanoDesu) - GJ-Bu'                                            : pfuncs.extractBase,
				'(NanoDesu) - Hai to Gensou no Grimgal'                         : pfuncs.extractBase,
				'(NanoDesu) - Hentai Ouji to Warawanai Neko'                    : pfuncs.extractBase,
				'(NanoDesu) - Kono Sekai ga Game Dato Ore Dake ga Shitteiru'    : pfuncs.extractBase,
				'(NanoDesu) - Kore wa Zombie Desu ka?'                          : pfuncs.extractBase,
				'(NanoDesu) - Kurenai'                                          : pfuncs.extractBase,
				'(NanoDesu) - Love★You'                                        : pfuncs.extractBase,
				'(NanoDesu) - Maoyuu Maou Yuusha'                               : pfuncs.extractBase,
				'(NanoDesu) - Mayo Chiki'                                       : pfuncs.extractBase,
				'(NanoDesu) - Ojamajo Doremi'                                   : pfuncs.extractBase,
				'(NanoDesu) - Oreimo'                                           : pfuncs.extractBase,
				'(NanoDesu) - Rokka no Yuusha'                                  : pfuncs.extractBase,
				'(NanoDesu) - Saenai Heroine no Sodatekata'                     : pfuncs.extractBase,
				'(NanoDesu) - Sasami-San@Ganbaranai'                            : pfuncs.extractBase,
				'(NanoDesu) - Seitokai no Ichizon'                              : pfuncs.extractBase,
				'(NanoDesu) - Sky World'                                        : pfuncs.extractBase,
				'(NanoDesu) - Yahari Ore no Seishun Love Come wa Machigatteiru' : pfuncs.extractBase,
				'-Sloth-'                                                       : pfuncs.extractBase,
				'12 Superlatives'                                               : pfuncs.extractBase,
				'77 Novel'                                                      : pfuncs.extractBase,
				'[G.O] Chronicles'                                              : pfuncs.extractBase,
				'[nakulas]'                                                     : pfuncs.extractBase,
				'A Pearly View'                                                 : pfuncs.extractBase,
				'A Translator\'s Ramblings'                                     : pfuncs.extractBase,
				'A traveler\'s translations.'                                   : pfuncs.extractBase,
				'Adamantine Dragon in the Crystal World'                        : pfuncs.extractBase,
				'alicetranslations.wordpress.com'                               : pfuncs.extractBase,
				'All\'s Fair In Love & War'                                     : pfuncs.extractBase,
				'Anon Empire'                                                   : pfuncs.extractBase,
				'Aori Translations'                                             : pfuncs.extractBase,
				'Aqua Scans'                                                    : pfuncs.extractBase,
				'Archivity'                                                     : pfuncs.extractBase,
				'Bear Bear Translations'                                        : pfuncs.extractBase,
				'BeRsErk Translations'                                          : pfuncs.extractBase,
				'C Novels 2 C'                                                  : pfuncs.extractBase,
				'Cat Scans'                                                     : pfuncs.extractBase,
				'cavescans.com'                                                 : pfuncs.extractBase,
				'Cheddar!'                                                      : pfuncs.extractBase,
				'Chinese Weaboo Translations'                                   : pfuncs.extractBase,
				'Circle of Shards'                                              : pfuncs.extractBase,
				'Cloud Manor'                                                   : pfuncs.extractBase,
				'Code-Zero\'s Blog'                                             : pfuncs.extractBase,
				'Cosmic Translation'                                            : pfuncs.extractBase,
				'Currently TLing [Bu ni Mi]'                                    : pfuncs.extractBase,
				'Deadly Forgotten Legends'                                      : pfuncs.extractBase,
				'Defan\'s Translations'                                         : pfuncs.extractBase,
				'Descent Subs'                                                  : pfuncs.extractBase,
				'Dorayakiz'                                                     : pfuncs.extractBase,
				'Dream Avenue'                                                  : pfuncs.extractBase,
				'Duran Daru Translation'                                        : pfuncs.extractBase,
				'Durasama'                                                      : pfuncs.extractBase,
				'EC Webnovel'                                                   : pfuncs.extractBase,
				'ELYSION Translation'                                           : pfuncs.extractBase,
				'Emergency Exit\'s Release Blog'                                : pfuncs.extractBase,
				'EndKun'                                                        : pfuncs.extractBase,
				'Ente38 translations'                                           : pfuncs.extractBase,
				'Epyon Translations'                                            : pfuncs.extractBase,
				'eternalpath.net'                                               : pfuncs.extractBase,
				'Etheria Translations'                                          : pfuncs.extractBase,
				'Eugene Rain'                                                   : pfuncs.extractBase,
				'Eye of Adventure '                                             : pfuncs.extractBase,
				'EZ Translations'                                               : pfuncs.extractBase,
				'Fighting Dreamers Scanlations'                                 : pfuncs.extractBase,
				'Flicker Hero'                                                  : pfuncs.extractBase,
				'Fung Shen'                                                     : pfuncs.extractFungShen,
				'Fuzion Life'                                                   : pfuncs.extractBase,
				'Gargoyle Web Serial'                                           : pfuncs.extractBase,
				'Grow with me'                                                  : pfuncs.extractBase,
				'Hamster428'                                                    : pfuncs.extractBase,
				'Heart Crusade Scans'                                           : pfuncs.extractBase,
				'Hello Translations'                                            : pfuncs.extractBase,
				'Hellping'                                                      : pfuncs.extractBase,
				'Hendricksen-sama'                                              : pfuncs.extractBase,
				'Infinite Translations'                                         : pfuncs.extractBase,
				'Isolarium'                                                     : pfuncs.extractBase,
				'Istian\'s Workshop'                                            : pfuncs.extractBase,
				'itranslateln'                                                  : pfuncs.extractBase,
				'Jagaimo'                                                       : pfuncs.extractBase,
				'Kedelu'                                                        : pfuncs.extractBase,
				'Kisato\'s MLTs'                                                : pfuncs.extractBase,
				'KN Translation'                                                : pfuncs.extractBase,
				'Knokkro Translations'                                          : pfuncs.extractBase,
				'Krytyk\'s Translations'                                        : pfuncs.extractBase,
				'Kuma Otou'                                                     : pfuncs.extractBase,
				'Kurotsuki Novel'                                               : pfuncs.extractBase,
				'Kyakka Translations'                                           : pfuncs.extractBase,
				'L2M'                                                           : pfuncs.extractBase,
				'Lastvoice Translator'                                          : pfuncs.extractBase,
				'Layzisheep'                                                    : pfuncs.extractBase,
				'Light Novel translations'                                      : pfuncs.extractBase,
				'Lil\' Bliss Novels'                                            : pfuncs.extractBase,
				'Linked Translations'                                           : pfuncs.extractBase,
				'Lizard Translations'                                           : pfuncs.extractBase,
				'LMS Machine Translations'                                      : pfuncs.extractBase,
				'LorCromwell'                                                   : pfuncs.extractBase,
				'Maou na Anoko to murabito a'                                   : pfuncs.extractBase,
				'Martial God Translator'                                        : pfuncs.extractBase,
				'Midnight Translation Blog'                                     : pfuncs.extractBase,
				'Mnemeaa'                                                       : pfuncs.extractBase,
				'mousou-haven.com'                                              : pfuncs.extractBase,
				'Mystique Translations'                                         : pfuncs.extractBase,
				'n00btranslations.wordpress.com'                                : pfuncs.extractBase,
				'NanoDesu Light Novel Translations'                             : pfuncs.extractBase,
				'National NEET'                                                 : pfuncs.extractBase,
				'NOT Daily Translations'                                        : pfuncs.extractBase,
				'Nowhere & Nothing'                                             : pfuncs.extractBase,
				'omatranslations.wordpress.com'                                 : pfuncs.extractBase,
				'Ore ga Heroine in English'                                     : pfuncs.extractBase,
				'Otome Revolution'                                              : pfuncs.extractBase,
				'Pact Web Serial'                                               : pfuncs.extractBase,
				'Paztok'                                                        : pfuncs.extractBase,
				'Pea Translation'                                               : pfuncs.extractBase,
				'Pielord Translations'                                          : pfuncs.extractBase,
				'Polyphonic Story Translation Group'                            : pfuncs.extractBase,
				'Popsiclete'                                                    : pfuncs.extractBase,
				'Project Accelerator'                                           : pfuncs.extractBase,
				'Pumpkin Translations'                                          : pfuncs.extractBase,
				'Quality ★ Mistranslations'                                    : pfuncs.extractBase,
				'Raising Angels & Defection'                                    : pfuncs.extractBase,
				'Reject Hero'                                                   : pfuncs.extractBase,
				'Romantic Dreamer\'s Sanctuary'                                 : pfuncs.extractBase,
				'Rosyfantasy - Always Dreaming'                                 : pfuncs.extractBase,
				'Rumanshi\'s Lair'                                              : pfuncs.extractBase,
				'Saber Translations'                                            : pfuncs.extractBase,
				'Sauri\'s TL Blog'                                              : pfuncs.extractBase,
				'SETSUNA86BLOG'                                                 : pfuncs.extractBase,
				'Sherma Translations'                                           : pfuncs.extractBase,
				'Shokyuu Translations'                                          : pfuncs.extractBase,
				'Silver Butterfly'                                              : pfuncs.extractBase,
				'Slime Lv1'                                                     : pfuncs.extractBase,
				'Snow & Dust'                                                   : pfuncs.extractBase,
				'soaringtranslations.wordpress.com'                             : pfuncs.extractBase,
				'solitarytranslation.wordpress.com'                             : pfuncs.extractBase,
				'Stellar Transformation Con.'                                   : pfuncs.extractBase,
				'STL Translations'                                              : pfuncs.extractBase,
				'Stone Burners'                                                 : pfuncs.extractBase,
				'Sun Shower Fields'                                             : pfuncs.extractBase,
				'Super Potato Translations'                                     : pfuncs.extractBase,
				'Symbiote'                                                      : pfuncs.extractBase,
				'tap-trans » tappity tappity tap.'                              : pfuncs.extractBase,
				'Terminus Translation'                                          : pfuncs.extractBase,
				'The Named'                                                     : pfuncs.extractBase,
				'The Sphere'                                                    : pfuncs.extractBase,
				'TheDefend Translations'                                        : pfuncs.extractBase,
				'Tieshaunn'                                                     : pfuncs.extractBase,
				'Tofubyu'                                                       : pfuncs.extractBase,
				'Translation Treasure Box'                                      : pfuncs.extractBase,
				'Translations From Outer Space'                                 : pfuncs.extractBase,
				'Tumble Into Fantasy'                                           : pfuncs.extractBase,
				'Tus-Trans'                                                     : pfuncs.extractBase,
				'U Donate We Translate'                                         : pfuncs.extractBase,
				'Unlimited Story Works'                                         : pfuncs.extractBase,
				'Useless no 4'                                                  : pfuncs.extractBase,
				'Village Translations'                                          : pfuncs.extractBase,
				'walkthejianghu.wordpress.com'                                  : pfuncs.extractBase,
				'Watermelon Helmets'                                            : pfuncs.extractBase,
				'Weaving stories and building castles in the clouds'            : pfuncs.extractBase,
				'Wele Translation'                                              : pfuncs.extractBase,
				'When The Hunting Party Came'                                   : pfuncs.extractBase,
				'Whimsical Land'                                                : pfuncs.extractBase,
				'White Tiger Translations'                                      : pfuncs.extractBase,
				'Word of Craft'                                                 : pfuncs.extractBase,
				'World of Summie'                                               : pfuncs.extractBase,
				'Worm - A Complete Web Serial'                                  : pfuncs.extractBase,
				'Wuxiwish'                                                      : pfuncs.extractBase,
				'www.pridesfamiliarsmaidens.com'                                : pfuncs.extractBase,
				'www.soltarination.org'                                         : pfuncs.extractBase,
				'xantbos.wordpress.com'                                         : pfuncs.extractBase,
				'Yet Another Translation Site'                                  : pfuncs.extractBase,
				'Yi Yue Translation'                                            : pfuncs.extractBase,
				'youtsubasilver\'s Blog'                                        : pfuncs.extractBase,
				'Zen Translations'                                              : pfuncs.extractBase,

				'ヾ(。￣□￣)ﾂ'                                                    : pfuncs.extractBase,
				'一期一会, 万歳!'                                                : pfuncs.extractBase,
				'睡眠中毒'                                                       : pfuncs.extractBase,
				'輝く世界'                                                        : pfuncs.extractBase,


				'tiffybook.com'                                                 : pfuncs.extractCrazyForHENovels,
				'Crazy for HE Novels'                                           : pfuncs.extractCrazyForHENovels,

				# No Posts yet?
				'Novel Trans'                                                   : pfuncs.extractBase,
				'The Bathrobe Knight'                                           : pfuncs.extractBathrobeKnight,
				'Dramas, Books & Tea'                                           : pfuncs.extractDramasBooksTea,

				# Not parseable.
				'Crack of Dawn Translations'                                    : pfuncs.extractCrackofDawnTranslations,
		}



		if item['srcname'] in funcMap:
			ret = funcMap[item['srcname']](item)
		else:
			print("No filter found?")

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
		return json.dumps(ret)

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

		if tx_raw:
			raw = self.getRawFeedMessage(feedDat)
			if raw:
				self.amqp_put_item(raw)

		if tx_parse:
			new = self.getProcessedReleaseInfo(feedDat)
			if new:
				self.amqp_put_item(new)

