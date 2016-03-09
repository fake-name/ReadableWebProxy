
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
				'Dark Translations'                                             : pfuncs.extractDarkTranslations,
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
				'Epyon Translations'                                            : pfuncs.extractEpyonTranslations,
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
				'Fung Shen'                                                     : pfuncs.extractFungShen,
				'Gila Translation Monster'                                      : pfuncs.extractGilaTranslation,
				'Giraffe Corps'                                                 : pfuncs.extractGiraffe,
				'Goddess! Grant Me a Girlfriend!!'                              : pfuncs.extractGoddessGrantMeaGirlfriend,
				'Gravity Tales'                                                 : pfuncs.extractGravityTranslation,
				'Grow with Me'                                                  : pfuncs.extractGrowWithMe,
				'guhehe.TRANSLATIONS'                                           : pfuncs.extractGuhehe,
				'Guro Translation'                                              : pfuncs.extractGuroTranslation,
				'Hajiko translation'                                            : pfuncs.extractHajiko,
				'HaruPARTY'                                                     : pfuncs.extractHaruPARTY,
				'Helidwarf'                                                     : pfuncs.extractHelidwarf,
				'Henouji Translation'                                           : pfuncs.extractHenoujiTranslation,
				'Heroic Novels'                                                 : pfuncs.extractHeroicNovels,
				'Hokage Translations'                                           : pfuncs.extractHokageTrans,
				'Hold \'X\' and Click'                                          : pfuncs.extractHoldX,
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
				'Knokkro Translations'                                          : pfuncs.extractKnokkroTranslations,
				'KobatoChanDaiSukiScan'                                         : pfuncs.extractKobatoChanDaiSukiScan,
				'Konobuta'                                                      : pfuncs.extractKonobuta,
				'Kore Yori Hachidori'                                           : pfuncs.extractKoreYoriHachidori,
				'Korean Novel Translations'                                     : pfuncs.extractKoreanNovelTrans,
				'Kuma Otou'                                                     : pfuncs.extractKumaOtou,
				'Kyakka'                                                        : pfuncs.extractKyakka,
				'Larvyde'                                                       : pfuncs.extractLarvyde,
				'Lascivious Imouto'                                             : pfuncs.extractLasciviousImouto,
				'Lazy NEET Translations'                                        : pfuncs.extractNEET,
				'Legend of Galactic Heroes Translation Project'                 : pfuncs.extractLegendofGalacticHeroes,
				'Lil\' Bliss Novels'                                            : pfuncs.extractLilBlissNovels,
				'Lingson\'s Translations'                                       : pfuncs.extractLingson,
				'Linked Translations'                                           : pfuncs.extractLinkedTranslations,
				'Ln Addiction'                                                  : pfuncs.extractLnAddiction,
				'Loiterous'                                                     : pfuncs.extractLoiterous,
				'Lonahora'                                                      : pfuncs.extractLonahora,
				'Lost in Translation'                                           : pfuncs.extractLostInTranslation,
				'Luen Translations'                                             : pfuncs.extractLuenTranslations,
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
				'NOT Daily Translations'                                        : pfuncs.extractNotDailyTranslations,
				'Novel Saga'                                                    : pfuncs.extractNovelSaga,
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
				'Pea\'s Kingdom'                                                : pfuncs.extractPeasKingdom,
				'Pika Translations'                                             : pfuncs.extractPikaTranslations,
				'Pippi Site'                                                    : pfuncs.extractPippiSite,
				'PlainlyBored'                                                  : pfuncs.extractPlainlyBored,
				'Priddles Translations'                                         : pfuncs.extractPriddlesTranslations,
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
				'Rosyfantasy - Always Dreaming'                                 : pfuncs.extractRosyfantasy,
				'Roxism HQ'                                                     : pfuncs.extractRoxism,
				'Rumanshi\'s Lair'                                              : pfuncs.extractRumanshisLair,
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
				'Sora Translations'                                             : pfuncs.extractSoraTranslations,
				'Sousetsuka'                                                    : pfuncs.extractSousetsuka,
				'Subudai11'                                                     : pfuncs.extractSubudai11,
				'Supreme Origin Translations'                                   : pfuncs.extractSotranslations,
				'Suteki Da Ne'                                                  : pfuncs.extractSutekiDaNe,
				'Sword and Game'                                                : pfuncs.extractSwordAndGame,
				'Sylver Translations'                                           : pfuncs.extractSylver,
				'Taint'                                                         : pfuncs.extractTaint,
				'Tales of MU'                                                   : pfuncs.extractTalesOfMU,
				'Tensai Translations'                                           : pfuncs.extractTensaiTranslations,
				'ThatGuyOverThere'                                              : pfuncs.extractThatGuyOverThere,
				'The Beginning After The End'                                   : pfuncs.extractBeginningAfterTheEnd,
				'The C-Novel Project'                                           : pfuncs.extractCNovelProj,
				'The Mustang Translator'                                        : pfuncs.extractTheMustangTranslator,
				'The Tales of Paul Twister'                                     : pfuncs.extractTalesOfPaulTwister,
				'The Zombie Knight'                                             : pfuncs.extractZombieKnight,
				'TheLazy9'                                                      : pfuncs.extractTheLazy9,
				'Light Novels Translations'                                     : pfuncs.extractLightNovelsTranslations,
				'Thunder Translation'                                           : pfuncs.extractThunder,
				'Thyaeria Translations'                                         : pfuncs.extractThyaeria,
				'Tomorolls'                                                     : pfuncs.extractTomorolls,
				'Tony Yon Ka'                                                   : pfuncs.extractTonyYonKa,
				'Totally Insane Tranlation'                                     : pfuncs.extractTotallyInsaneTranslation,
				'Totally Insane Translation'                                    : pfuncs.extractTotallyInsaneTranslation,
				'EccentricTranslations'                                         : pfuncs.extractEccentricTranslations,
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
				'U Donate We Translate'                                         : pfuncs.extractUDonateWeTranslate,
				'Ultimate Arcane'                                               : pfuncs.extractUltimateArcane,
				'Unchained Translation'                                         : pfuncs.extractUnchainedTranslation,
				'Universes With Meaning'                                        : pfuncs.extractUniversesWithMeaning,
				'Untuned Translation Blog'                                      : pfuncs.extractUntunedTranslation,
				'VaanCruze'                                                     : pfuncs.extractMaouTheYuusha,
				'Verathragana Stories'                                          : pfuncs.extractVerathragana,
				'Void Translations'                                             : pfuncs.extractVoidTranslations,
				'Volare Translations'                                           : pfuncs.extractVolareTranslations,
				'Walk the Jiang Hu'                                             : pfuncs.extractWalkTheJiangHu,
				'Walking the Storm'                                             : pfuncs.extractWalkingTheStorm,
				'Wat Da Meow'                                                   : pfuncs.extractWatDaMeow,
				'Watermelon Helmets'                                            : pfuncs.extractWatermelonHelmets,
				'WCC Translation'                                               : pfuncs.extractWCCTranslation,
				'Web Novel Japanese Translation'                                : pfuncs.extractWebNovelJapaneseTranslation,
				'Wele Translation'                                              : pfuncs.extractWeleTranslation,
				'White Tiger Translations'                                      : pfuncs.extractWhiteTigerTranslations,
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
				'Youko Advent'                                                  : pfuncs.extractYoukoAdvent,
				'Youshoku Translations'                                         : pfuncs.extractYoushoku,
				'Willful Casual'                                                : pfuncs.extractWillfulCasual,
				'Yukkuri Free Time Literature Service'                          : pfuncs.extractYukkuri,
				'IntenseDesSugar'                                               : pfuncs.extractIntenseDesSugar,
				'Ziru\'s Musings | Translations~'                               : pfuncs.extractZiruTranslations,
				'ZSW'                                                           : pfuncs.extractZSW,
				'~Taffy Translations~'                                          : pfuncs.extractTaffyTranslations,
				'ℝeanとann@'                                                     : pfuncs.extractReantoAnna,
				'お兄ちゃん、やめてぇ！'                                               : pfuncs.extractOniichanyamete,
				'中翻英圖書館 Translations'                                       : pfuncs.extractTuShuGuan,
				'桜翻訳! | Light novel translations'                             : pfuncs.extractSakurahonyaku,
				'pandafuqtranslations'                                          : pfuncs.extractPandafuqTranslations,
				'Paztok'                                                        : pfuncs.extractPaztok,
				'EC Webnovel'                                                   : pfuncs.extractECWebnovel,


				# KnW mess
				'Blazing Translations'                                          : pfuncs.extractKnW,
				'CapsUsingShift Tl'                                             : pfuncs.extractKnW,
				'Insignia Pierce'                                               : pfuncs.extractKnW,
				'Kiriko Translations'                                           : pfuncs.extractKnW,
				'Konjiki no Wordmaster'                                         : pfuncs.extractKnW,
				'Loliquent'                                                     : pfuncs.extractKnW,
				'Pummels Translations'                                          : pfuncs.extractKnW,
				'XCrossJ'                                                       : pfuncs.extractKnW,


				'Ducky\'s English Translations'                                 : pfuncs.extractDuckysEnglishTranslations,
				'Bad Translation'                                               : pfuncs.extractBadTranslation,
				'LordofScrubs'                                                  : pfuncs.extractLordofScrubs,
				'Roasted Tea'                                                   : pfuncs.extractRoastedTea,
				'Undecent Translations'                                         : pfuncs.extractUndecentTranslations,
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
				'(NanoDesu) - Love★You'                                        : pfuncs.extractNanoDesuLoveYou,
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
				'12 Superlatives'                                               : pfuncs.extract12Superlatives,
				'77 Novel'                                                      : pfuncs.extract77Novel,
				'[G.O] Chronicles'                                              : pfuncs.extractGOChronicles,
				'[nakulas]'                                                     : pfuncs.extractNakulas,
				'A Pearly View'                                                 : pfuncs.extractAPearlyView,
				'A Translator\'s Ramblings'                                     : pfuncs.extractATranslatorsRamblings,
				'A traveler\'s translations.'                                   : pfuncs.extractATravelersTranslations,
				'Adamantine Dragon in the Crystal World'                        : pfuncs.extractAdamantineDragonintheCrystalWorld,
				'alicetranslations.wordpress.com'                               : pfuncs.extractAlicetranslations,
				'All\'s Fair In Love & War'                                     : pfuncs.extractAllsFairInLoveWar,
				'Anon Empire'                                                   : pfuncs.extractAnonEmpire,
				'Aori Translations'                                             : pfuncs.extractAoriTranslations,
				'Aqua Scans'                                                    : pfuncs.extractAquaScans,
				'Archivity'                                                     : pfuncs.extractArchivity,
				'Bear Bear Translations'                                        : pfuncs.extractBearBearTranslations,
				'BeRsErk Translations'                                          : pfuncs.extractBeRsErkTranslations,
				'C Novels 2 C'                                                  : pfuncs.extractCNovels2C,
				'Cat Scans'                                                     : pfuncs.extractCatScans,
				'cavescans.com'                                                 : pfuncs.extractCavescans,
				'Cheddar!'                                                      : pfuncs.extractCheddar,
				'Chinese Weaboo Translations'                                   : pfuncs.extractChineseWeabooTranslations,
				'Circle of Shards'                                              : pfuncs.extractCircleofShards,
				'Cloud Manor'                                                   : pfuncs.extractCloudManor,
				'Code-Zero\'s Blog'                                             : pfuncs.extractCodeZerosBlog,
				'Cosmic Translation'                                            : pfuncs.extractCosmicTranslation,
				'Currently TLing [Bu ni Mi]'                                    : pfuncs.extractCurrentlyTLingBuniMi,
				'Deadly Forgotten Legends'                                      : pfuncs.extractDeadlyForgottenLegends,
				'Defan\'s Translations'                                         : pfuncs.extractDefansTranslations,
				'Descent Subs'                                                  : pfuncs.extractDescentSubs,
				'Dorayakiz'                                                     : pfuncs.extractDorayakiz,
				'Dream Avenue'                                                  : pfuncs.extractDreamAvenue,
				'Duran Daru Translation'                                        : pfuncs.extractDuranDaruTranslation,
				'Durasama'                                                      : pfuncs.extractDurasama,
				'ELYSION Translation'                                           : pfuncs.extractELYSIONTranslation,
				'Emergency Exit\'s Release Blog'                                : pfuncs.extractEmergencyExitsReleaseBlog,
				'EndKun'                                                        : pfuncs.extractEndKun,
				'Ente38 translations'                                           : pfuncs.extractEnte38translations,
				'eternalpath.net'                                               : pfuncs.extractEternalpath,
				'Etheria Translations'                                          : pfuncs.extractEtheriaTranslations,
				'Eugene Rain'                                                   : pfuncs.extractEugeneRain,
				'Eye of Adventure '                                             : pfuncs.extractEyeofAdventure,
				'EZ Translations'                                               : pfuncs.extractEZTranslations,
				'Fighting Dreamers Scanlations'                                 : pfuncs.extractFightingDreamersScanlations,
				'Flicker Hero'                                                  : pfuncs.extractFlickerHero,
				'Fuzion Life'                                                   : pfuncs.extractFuzionLife,
				'Gargoyle Web Serial'                                           : pfuncs.extractGargoyleWebSerial,
				'Hamster428'                                                    : pfuncs.extractHamster428,
				'Heart Crusade Scans'                                           : pfuncs.extractHeartCrusadeScans,
				'Hello Translations'                                            : pfuncs.extractHelloTranslations,
				'Hellping'                                                      : pfuncs.extractHellping,
				'Hendricksen-sama'                                              : pfuncs.extractHendricksensama,
				'Infinite Translations'                                         : pfuncs.extractInfiniteTranslations,
				'Isolarium'                                                     : pfuncs.extractIsolarium,
				'Istian\'s Workshop'                                            : pfuncs.extractIstiansWorkshop,
				'itranslateln'                                                  : pfuncs.extractItranslateln,
				'Jagaimo'                                                       : pfuncs.extractJagaimo,
				'Kedelu'                                                        : pfuncs.extractKedelu,
				'Kisato\'s MLTs'                                                : pfuncs.extractKisatosMLTs,
				'KN Translation'                                                : pfuncs.extractKNTranslation,
				'Krytyk\'s Translations'                                        : pfuncs.extractKrytyksTranslations,
				'Kurotsuki Novel'                                               : pfuncs.extractKurotsukiNovel,
				'Kyakka Translations'                                           : pfuncs.extractKyakkaTranslations,
				'L2M'                                                           : pfuncs.extractL2M,
				'Lastvoice Translator'                                          : pfuncs.extractLastvoiceTranslator,
				'Layzisheep'                                                    : pfuncs.extractLayzisheep,
				'Light Novel translations'                                      : pfuncs.extractLightNoveltranslations,
				'Lizard Translations'                                           : pfuncs.extractLizardTranslations,
				'LMS Machine Translations'                                      : pfuncs.extractLMSMachineTranslations,
				'LorCromwell'                                                   : pfuncs.extractLorCromwell,
				'Maou na Anoko to murabito a'                                   : pfuncs.extractMaounaAnokotomurabitoa,
				'Martial God Translator'                                        : pfuncs.extractMartialGodTranslator,
				'Midnight Translation Blog'                                     : pfuncs.extractMidnightTranslationBlog,
				'Mnemeaa'                                                       : pfuncs.extractMnemeaa,
				'mousou-haven.com'                                              : pfuncs.extractMousouhaven,
				'Mystique Translations'                                         : pfuncs.extractMystiqueTranslations,
				'NanoDesu Light Novel Translations'                             : pfuncs.extractNanoDesuLightNovelTranslations,
				'National NEET'                                                 : pfuncs.extractNationalNEET,
				'Nowhere & Nothing'                                             : pfuncs.extractNowhereNothing,
				'Ore ga Heroine in English'                                     : pfuncs.extractOregaHeroineinEnglish,
				'Otome Revolution'                                              : pfuncs.extractOtomeRevolution,
				'Pact Web Serial'                                               : pfuncs.extractPactWebSerial,
				'Pea Translation'                                               : pfuncs.extractPeaTranslation,
				'Pielord Translations'                                          : pfuncs.extractPielordTranslations,
				'Polyphonic Story Translation Group'                            : pfuncs.extractPolyphonicStoryTranslationGroup,
				'Popsiclete'                                                    : pfuncs.extractPopsiclete,
				'Project Accelerator'                                           : pfuncs.extractProjectAccelerator,
				'Pumpkin Translations'                                          : pfuncs.extractPumpkinTranslations,
				'Quality ★ Mistranslations'                                    : pfuncs.extractQualityMistranslations,
				'Raising Angels & Defection'                                    : pfuncs.extractRaisingAngelsDefection,
				'Reject Hero'                                                   : pfuncs.extractRejectHero,
				'Romantic Dreamer\'s Sanctuary'                                 : pfuncs.extractRomanticDreamersSanctuary,
				'Saber Translations'                                            : pfuncs.extractSaberTranslations,
				'Sauri\'s TL Blog'                                              : pfuncs.extractSaurisTLBlog,
				'SETSUNA86BLOG'                                                 : pfuncs.extractSETSUNA86BLOG,
				'Sherma Translations'                                           : pfuncs.extractShermaTranslations,
				'Shokyuu Translations'                                          : pfuncs.extractShokyuuTranslations,
				'Silver Butterfly'                                              : pfuncs.extractSilverButterfly,
				'Slime Lv1'                                                     : pfuncs.extractSlimeLv1,
				'Snow & Dust'                                                   : pfuncs.extractSnowDust,
				'Stellar Transformation Con.'                                   : pfuncs.extractStellarTransformationCon,
				'STL Translations'                                              : pfuncs.extractSTLTranslations,
				'Stone Burners'                                                 : pfuncs.extractStoneBurners,
				'Sun Shower Fields'                                             : pfuncs.extractSunShowerFields,
				'Super Potato Translations'                                     : pfuncs.extractSuperPotatoTranslations,
				'Symbiote'                                                      : pfuncs.extractSymbiote,
				'tap-trans » tappity tappity tap.'                              : pfuncs.extractTaptrans,
				'Terminus Translation'                                          : pfuncs.extractTerminusTranslation,
				'The Named'                                                     : pfuncs.extractTheNamed,
				'The Sphere'                                                    : pfuncs.extractTheSphere,
				'TheDefend Translations'                                        : pfuncs.extractTheDefendTranslations,
				'Tieshaunn'                                                     : pfuncs.extractTieshaunn,
				'Tofubyu'                                                       : pfuncs.extractTofubyu,
				'Translation Treasure Box'                                      : pfuncs.extractTranslationTreasureBox,
				'Translations From Outer Space'                                 : pfuncs.extractTranslationsFromOuterSpace,
				'Tumble Into Fantasy'                                           : pfuncs.extractTumbleIntoFantasy,
				'Tus-Trans'                                                     : pfuncs.extractTusTrans,
				'Unlimited Story Works'                                         : pfuncs.extractUnlimitedStoryWorks,
				'Useless no 4'                                                  : pfuncs.extractUselessno4,
				'Village Translations'                                          : pfuncs.extractVillageTranslations,
				'Weaving stories and building castles in the clouds'            : pfuncs.extractWeavingstoriesandbuildingcastlesintheclouds,
				'When The Hunting Party Came'                                   : pfuncs.extractWhenTheHuntingPartyCame,
				'Whimsical Land'                                                : pfuncs.extractWhimsicalLand,
				'Word of Craft'                                                 : pfuncs.extractWordofCraft,
				'World of Summie'                                               : pfuncs.extractWorldofSummie,
				'Worm - A Complete Web Serial'                                  : pfuncs.extractWormACompleteWebSerial,
				'Wuxiwish'                                                      : pfuncs.extractWuxiwish,
				'www.pridesfamiliarsmaidens.com'                                : pfuncs.extractPridesFamiliarsMaidens,
				'www.soltarination.org'                                         : pfuncs.extractSoltarination,
				'xantbos.wordpress.com'                                         : pfuncs.extractXantbos,
				'Yi Yue Translation'                                            : pfuncs.extractYiYueTranslation,
				'youtsubasilver\'s Blog'                                        : pfuncs.extractYoutsubasilversBlog,
				'Zen Translations'                                              : pfuncs.extractZenTranslations,
				'The Beginning After The End Novel'                             : pfuncs.extractTheBeginningAfterTheEnd,


				"Cautr's"                                                       : pfuncs.extractCautrs,
				"DOW's Translations"                                            : pfuncs.extractDOWsTranslations,
				"Hon'yaku"                                                      : pfuncs.extractHonyaku,
				"Pandora's Book"                                                : pfuncs.extractPandorasBook,
				"Rui's Translations"                                            : pfuncs.extractRuisTranslations,
				"WizThief's Novels"                                             : pfuncs.extractWizThiefsNovels,
				'Another Parallel World'                                        : pfuncs.extractAnotherParallelWorld,
				'Another World Translations'                                    : pfuncs.extractAnotherWorldTranslations,
				'Ayax World'                                                    : pfuncs.extractAyaxWorld,
				'Bijinsans'                                                     : pfuncs.extractBijinsans,
				'Bluefire Translations'                                         : pfuncs.extractBluefireTranslations,
				'Chrona Zero'                                                   : pfuncs.extractChronaZero,
				'Chronon Translations'                                          : pfuncs.extractChrononTranslations,
				'Cloud Translations'                                            : pfuncs.extractCloudTranslations,
				'CookiePasta Translations'                                      : pfuncs.extractCookiePastaTranslations,
				'Crappy Machine Translation'                                    : pfuncs.extractCrappyMachineTranslation,
				'Daily-Dallying'                                                : pfuncs.extractDailyDallying,
				'Dekinai Diary'                                                 : pfuncs.extractDekinaiDiary,
				'Disappointing Translations'                                    : pfuncs.extractDisappointingTranslations,
				'Fake typist'                                                   : pfuncs.extractFaketypist,
				'Falamar Translation'                                           : pfuncs.extractFalamarTranslation,
				'Falinmer'                                                      : pfuncs.extractFalinmer,
				'Gaochao Translations'                                          : pfuncs.extractGaochaoTranslations,
				'Hyorinmaru Blog'                                               : pfuncs.extractHyorinmaruBlog,
				'Januke Translations'                                           : pfuncs.extractJanukeTranslations,
				'Joie de Vivre'                                                 : pfuncs.extractJoiedeVivre,
				'Kakkokari'                                                     : pfuncs.extractKakkokari,
				'Kokuma Translations'                                           : pfuncs.extractKokumaTranslations,
				'Lickymee Translations'                                         : pfuncs.extractLickymeeTranslations,
				'Little Translations'                                           : pfuncs.extractLittleTranslations,
				'Lynfamily'                                                     : pfuncs.extractLynfamily,
				'Nakimushi'                                                     : pfuncs.extractNakimushi,
				'Nepustation'                                                   : pfuncs.extractNepustation,
				'NinjaNUF'                                                      : pfuncs.extractNinjaNUF,
				'Pekabo Blog'                                                   : pfuncs.extractPekaboBlog,
				'Penguin Overlord Translations'                                 : pfuncs.extractPenguinOverlordTranslations,
				'Pettanko Translations'                                         : pfuncs.extractPettankoTranslations,
				'Premium Red Tea'                                               : pfuncs.extractPremiumRedTea,
				'Psicern.Translations'                                          : pfuncs.extractPsicernTranslations,
				'Qualidea of Scum and a Gold Coin'                              : pfuncs.extractQualideaofScumandaGoldCoin,
				'Rip translations'                                              : pfuncs.extractRiptranslations,
				'Saiaku Translations Blog'                                      : pfuncs.extractSaiakuTranslationsBlog,
				'SenjiQ creations'                                              : pfuncs.extractSenjiQcreations,
				'Snowy Publications'                                            : pfuncs.extractSnowyPublications,
				'Solstar24'                                                     : pfuncs.extractSolstar24,
				'Spring Scents'                                                 : pfuncs.extractSpringScents,
				'Taida-dono Translations'                                       : pfuncs.extractTaidadonoTranslations,
				'Tales of The Forgottenslayer'                                  : pfuncs.extractTalesofTheForgottenslayer,
				'The Iron Teeth'                                                : pfuncs.extractTheIronTeeth,
				'This World Work'                                               : pfuncs.extractThisWorldWork,
				'TL Syosetsu'                                                   : pfuncs.extractTLSyosetsu,
				'Translating For Your Pleasure'                                 : pfuncs.extractTranslatingForYourPleasure,
				'Trung Nguyen'                                                  : pfuncs.extractTrungNguyen,
				'Turtle and Hare Translations'                                  : pfuncs.extractTurtleandHareTranslations,
				'Welcome To The Underdark'                                      : pfuncs.extractWelcomeToTheUnderdark,
				'Wuxia Translators'                                             : pfuncs.extractWuxiaTranslators,


				'ヾ(。￣□￣)ﾂ'                                                    : pfuncs.extractBase,
				'一期一会, 万歳!'                                                : pfuncs.extractBase,
				'睡眠中毒'                                                       : pfuncs.extractBase,
				'輝く世界'                                                        : pfuncs.extractBase,


				'Yet Another Translation Site'                                  : pfuncs.extractMiaomix539,
				'tiffybook.com'                                                 : pfuncs.extractCrazyForHENovels,
				'Crazy for HE Novels'                                           : pfuncs.extractCrazyForHENovels,

				# No Posts yet?
				'Novel Trans'                                                   : pfuncs.extractBase,
				'The Bathrobe Knight'                                           : pfuncs.extractBathrobeKnight,
				'Dramas, Books & Tea'                                           : pfuncs.extractDramasBooksTea,

				# Not parseable.
				'Crack of Dawn Translations'                                    : pfuncs.extractCrackofDawnTranslations,


				# MOAR
				"Evida's Indo Romance"                   : pfuncs.extractEvidasIndoRomance,
				"Xiaowen206's Blog"                      : pfuncs.extractXiaowen206sBlog,
				'A Grey World'                           : pfuncs.extractAGreyWorld,
				'Alice Translations'                     : pfuncs.extractAliceTranslations,
				'Aran Translations'                      : pfuncs.extractAranTranslations,
				'Ares Novels'                            : pfuncs.extractAresNovels,
				'Baka Pervert'                           : pfuncs.extractBakaPervert,
				'Blade of Hearts'                        : pfuncs.extractBladeOfHearts,
				'Blublub'                                : pfuncs.extractBlublub,
				'Books Movies and Beyond'                : pfuncs.extractBooksMoviesAndBeyond,
				'C-Novel Tranlations…'                   : pfuncs.extractCNovelTranlations,
				'CaveScans'                              : pfuncs.extractCaveScans,
				'ChubbyCheeks'                           : pfuncs.extractChubbyCheeks,
				'Distracted Chinese'                     : pfuncs.extractDistractedChinese,
				'fgiLaN translations'                    : pfuncs.extractfgiLaNTranslations,
				'GrimdarkZ Translations'                 : pfuncs.extractGrimdarkZTranslations,
				'Grow with me'                           : pfuncs.extractGrowWithMe,
				'Kuro Translations'                      : pfuncs.extractKuroTranslations,
				'Mousou Haven'                           : pfuncs.extractMousouHaven,
				'My Purple World'                        : pfuncs.extractMyPurpleWorld,
				'Mythical Pagoda'                        : pfuncs.extractMythicalPagoda,
				'N00b Translations'                      : pfuncs.extractN00bTranslations,
				'NovelCow'                               : pfuncs.extractNovelCow,
				'Opinisaya.com'                          : pfuncs.extractOpinisaya,
				'Patriarch Reliance'                     : pfuncs.extractPatriarchReliance,
				'Pride X ReVamp'                         : pfuncs.extractPrideXReVamp,
				'QualiTeaTranslations'                   : pfuncs.extractQualiTeaTranslations,
				'Rancer'                                 : pfuncs.extractRancer,
				'Root of Evil'                           : pfuncs.extractRootOfEvil,
				'Sloth Translations Blog'                : pfuncs.extractSlothTranslationsBlog,
				'Soltarination Scanlations'              : pfuncs.extractSoltarinationScanlations,
				'Sweet A Collections'                    : pfuncs.extractSweetACollections,
				'Ten Thousand Heaven Controlling Sword'  : pfuncs.extractTenThousandHeavenControllingSword,
				'The Asian Cult'                         : pfuncs.extractTheAsianCult,
				'The Last Skull'                         : pfuncs.extractTheLastSkull,
				'Towards the Sky~'                       : pfuncs.extractTowardsTheSky,
				'Trinity Archive'                        : pfuncs.extractTrinityArchive,
				'Tseirp Translations'                    : pfuncs.extractTseirpTranslations,
				'Xant Does Stuff and Things'             : pfuncs.extractXantDoesStuffAndThings,
				'Altoroc Translations'                   : pfuncs.extractAltorocTranslations,
				'Tentatively under construction'         : pfuncs.extractTentativelyUnderconstruction,
				'Tatakau Shisho Light Novel Translation' : pfuncs.extractTatakauShishoLightNovelTranslation,
				'Dragon MT'                              : pfuncs.extractDragonMT,


				'Zeonic'                                 : pfuncs.extractZeonic,
				'「\u3000」'                               : pfuncs.extractU3000,
				'Nanowave Translations'                  : pfuncs.extractNanowaveTranslations,
				'Heroic Legend of Arslan Translations'   : pfuncs.extractHeroicLegendOfArslanTranslations,
				"Dreamless Window's translation"         : pfuncs.extractDreamlessWindowsTranslation,
				'Koong Koong Translations'               : pfuncs.extractKoongKoongTranslations,
				'天才創造すなわち百合'                       : pfuncs.extract天才創造すなわち百合,
				'/'                                      : pfuncs.extractForwardSlash,
				'Keyo Translations'                      : pfuncs.extractKeyoTranslations,
				'Mojo Translations'                      : pfuncs.extractMojoTranslations,
				"Zxzxzx's blog"                          : pfuncs.extractZxzxzxsBlog,


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

