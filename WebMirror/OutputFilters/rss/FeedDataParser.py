
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
				'AFlappyTeddyBird'                                              : pfuncs.extractAFlappyTeddyBird,
				'Alcsel Translations'                                           : pfuncs.extractAlcsel,
				'Alyschu & Co'                                                  : pfuncs.extractAlyschuCo,
				'Ark Machine Translations'                                      : pfuncs.extractArkMachineTranslations,
				'AsherahBlue\'s Notebook'                                       : pfuncs.extractAsherahBlue,
				'Avert Translations'                                            : pfuncs.extractAvert,
				'Azure Sky Translation'                                         : pfuncs.extractAzureSky,
				'Baka Dogeza Translation'                                       : pfuncs.extractBakaDogeza,
				'Beehugger'                                                     : pfuncs.extractBeehugger,
				'Berseker Translations'                                         : pfuncs.extractBersekerTranslations,
				'Binggo&Corp'                                                   : pfuncs.extractBinggoCorp,
				'Binhjamin'                                                     : pfuncs.extractBinhjamin,
				'Blue Silver Translations'                                      : pfuncs.extractBlueSilverTranslations,
				'Bu Bu Jing Xin Translation'                                    : pfuncs.extractBuBuJingXinTrans,
				'Burei Dan Works'                                               : pfuncs.extractBureiDan,
				'C.E. Light Novel Translations'                                 : pfuncs.extractCeLn,
				'Calico x Tabby'                                                : pfuncs.extractCalicoxTabby,
				'Clicky Click Translation'                                      : pfuncs.extractClicky,
				'Defiring'                                                      : pfuncs.extractDefiring,
				'DragomirCM'                                                    : pfuncs.extractDragomirCM,
				'Dreadful Decoding'                                             : pfuncs.extractDreadfulDecoding,
				'Ensj Translations'                                             : pfuncs.extractEnsjTranslations,
				'EnTruce Translations'                                          : pfuncs.extractEnTruceTranslations,
				'Ero Light Novel Translations'                                  : pfuncs.extractEroLightNovelTranslations,
				'Eros Workshop'                                                 : pfuncs.extractErosWorkshop,
				'Fanatical'                                                     : pfuncs.extractFanatical,
				'FeedProxy'                                                     : pfuncs.extractFeedProxy,
				'Flower Bridge Too'                                             : pfuncs.extractFlowerBridgeToo,
				'Forgetful Dreamer'                                             : pfuncs.extractForgetfulDreamer,
				'Fudge Translations'                                            : pfuncs.extractFudgeTranslations,
				'Gila Translation Monster'                                      : pfuncs.extractGilaTranslation,
				'Giraffe Corps'                                                 : pfuncs.extractGiraffe,
				'Gravity Tales'                                                 : pfuncs.extractGravityTranslation,
				'guhehe.TRANSLATIONS'                                           : pfuncs.extractGuhehe,
				'Guro Translation'                                              : pfuncs.extractGuroTranslation,
				'Hajiko translation'                                            : pfuncs.extractHajiko,
				'Henouji Translation'                                           : pfuncs.extractHenoujiTranslation,
				'Hokage Translations'                                           : pfuncs.extractHokageTrans,
				'Imoutolicious Light Novel Translations'                        : pfuncs.extractImoutolicious,
				'Infinite Novel Translations'                                   : pfuncs.extractInfiniteNovelTranslations,
				'Isekai Mahou Translations!'                                    : pfuncs.extractIsekaiMahou,
				'Isekai Soul-Cyborg Translations'                               : pfuncs.extractIsekaiTranslation,
				'Iterations within a Thought-Eclipse'                           : pfuncs.extractIterations,
				'izra709 | B Group no Shounen Translations'                     : pfuncs.extractIzra709,
				'Japtem'                                                        : pfuncs.extractJaptem,
				'JawzTranslations'                                              : pfuncs.extractJawzTranslations,
				'Kaezar Translations'                                           : pfuncs.extractKaezar,
				'Kerambit\'s Incisions'                                         : pfuncs.extractKerambit,
				'Kiri Leaves'                                                   : pfuncs.extractKiri,
				'Kyakka'                                                        : pfuncs.extractKyakka,
				'Larvyde'                                                       : pfuncs.extractLarvyde,
				'Lazy NEET Translations'                                        : pfuncs.extractNEET,
				'Lingson\'s Translations'                                       : pfuncs.extractLingson,
				'Ln Addiction'                                                  : pfuncs.extractLnAddiction,
				'Lunate'                                                        : pfuncs.extractLunate,
				'LygarTranslations'                                             : pfuncs.extractLygarTranslations,
				'MadoSpicy TL'                                                  : pfuncs.extractMadoSpicy,
				'Mahou Koukoku'                                                 : pfuncs.extractMahouKoukoku,
				'Mahoutsuki Translation'                                        : pfuncs.extractMahoutsuki,
				'Manga0205 Translations'                                        : pfuncs.extractManga0205Translations,
				'Mike777ac'                                                     : pfuncs.extractMike777ac,
				'Moon Bunny Cafe'                                               : pfuncs.extractMoonBunnyCafe,
				'Natsu TL'                                                      : pfuncs.extractNatsuTl,
				'NEET Translations'                                             : pfuncs.extractNeetTranslations,
				'Neo Translations'                                              : pfuncs.extractNeoTranslations,
				'Nightbreeze Translations'                                      : pfuncs.extractNightbreeze,
				'Nohohon Translation'                                           : pfuncs.extractNohohon,
				'NoviceTranslator'                                              : pfuncs.extractNoviceTranslator,
				'Ohanashimi'                                                    : pfuncs.extractOhanashimi,
				'Omega Harem'                                                   : pfuncs.extractOmegaHarem,
				'otterspacetranslation'                                         : pfuncs.extractOtterspaceTranslation,
				'Pika Translations'                                             : pfuncs.extractPikaTranslations,
				'putttytranslations'                                            : pfuncs.extractPuttty,
				'Raising the Dead'                                              : pfuncs.extractRaisingTheDead,
				'RANCER'                                                        : pfuncs.extractRancer,
				'Rebirth Online'                                                : pfuncs.extractRebirthOnline,
				'Rhinabolla'                                                    : pfuncs.extractRhinabolla,
				'Rising Dragons Translation'                                    : pfuncs.extractRisingDragons,
				'Ruze Translations'                                             : pfuncs.extractRuzeTranslations,
				'Scrya Translations'                                            : pfuncs.extractScryaTranslations,
				'Shikkaku Translations'                                         : pfuncs.extractShikkakuTranslations,
				'Shin Translations'                                             : pfuncs.extractShinTranslations,
				'Shiroyukineko Translations'                                    : pfuncs.extractShiroyukineko,
				'Skythewood translations'                                       : pfuncs.extractSkythewood,
				'Sousetsuka'                                                    : pfuncs.extractSousetsuka,
				'Supreme Origin Translations'                                   : pfuncs.extractSotranslations,
				'Sword and Game'                                                : pfuncs.extractSwordAndGame,
				'Sylver Translations'                                           : pfuncs.extractSylver,
				'Tensai Translations'                                           : pfuncs.extractTensaiTranslations,
				'ThatGuyOverThere'                                              : pfuncs.extractThatGuyOverThere,
				'The C-Novel Project'                                           : pfuncs.extractCNovelProj,
				'TheLazy9'                                                      : pfuncs.extractTheLazy9,
				'Thunder Translation'                                           : pfuncs.extractThunder,
				'Tomorolls'                                                     : pfuncs.extractTomorolls,
				'Tony Yon Ka'                                                   : pfuncs.extractTonyYonKa,
				'Totokk\'s Translations'                                        : pfuncs.extractTotokk,
				'Translated by a Clown'                                         : pfuncs.extractClownTrans,
				'Translation Nations'                                           : pfuncs.extractTranslationNations,
				'Tripp Translations'                                            : pfuncs.extractTrippTl,
				'Tsuigeki Translations'                                         : pfuncs.extractTsuigeki,
				'Turb0 Translation'                                             : pfuncs.extractTurb0,
				'Unchained Translation'                                         : pfuncs.extractUnchainedTranslation,
				'Thyaeria Translations'                                         : pfuncs.extractThyaeria,
				'VaanCruze'                                                     : pfuncs.extractMaouTheYuusha,
				'Void Translations'                                             : pfuncs.extractVoidTranslations,
				'WCC Translation'                                               : pfuncs.extractWCCTranslation,
				'World of Watermelons'                                          : pfuncs.extractWatermelons,
				'Wuxia Translations'                                            : pfuncs.extractWuxiaTranslations,
				'Wuxiaworld'                                                    : pfuncs.extractWuxiaworld,
				'Yoraikun Translation'                                          : pfuncs.extractYoraikun,
				'Yukkuri Free Time Literature Service'                          : pfuncs.extractYukkuri,
				'Ziru\'s Musings | Translations~'                               : pfuncs.extractZiruTranslations,
				'お兄ちゃん、やめてぇ！'                                              : pfuncs.extractOniichanyamete,
				'中翻英圖書館 Translations'                                      : pfuncs.extractTuShuGuan,
				'桜翻訳! | Light novel translations'                             : pfuncs.extractSakurahonyaku,

				'Lonahora'                                                      : pfuncs.extractLonahora,
				'WuxiaSociety'                                                  : pfuncs.extractWuxiaSociety,
				'Wuxia Heroes'                                                  : pfuncs.extractWuxiaHeroes,
				'Radiant Translations'                                          : pfuncs.extractRadiantTranslations,
				'Tales of MU'                                                   : pfuncs.extractTalesOfMU,
				'ZSW'                                                           : pfuncs.extractZSW,

				'Youjinsite Translations'                                       : pfuncs.extractYoujinsite,
				'Youshoku Translations'                                         : pfuncs.extractYoushoku,
				'A0132'                                                         : pfuncs.extractA0132,
				'Lost in Translation'                                           : pfuncs.extractLostInTranslation,
				"Pea's Kingdom"                                                 : pfuncs.extractPeasKingdom,
				'Circus Translations'                                           : pfuncs.extractCircusTranslations,
				'Distracted Translations'                                       : pfuncs.extractDistractedTranslations,
				'Forgotten Conqueror'                                           : pfuncs.extractForgottenConqueror,
				"Hold 'X' and Click"                                            : pfuncs.extractHoldX,
				'Hot Cocoa Translations'                                        : pfuncs.extractHotCocoa,
				'Solitary Translation'                                          : pfuncs.extractSolitaryTranslation,
				'A Place Of Legends'                                            : pfuncs.extractPlaceOfLegends,

				# KnW mess
				'Blazing Translations'                                          : pfuncs.extractKnW,
				'CapsUsingShift Tl'                                             : pfuncs.extractKnW,
				'Insignia Pierce'                                               : pfuncs.extractKnW,
				'Kiriko Translations'                                           : pfuncs.extractKnW,
				'Konjiki no Wordmaster'                                         : pfuncs.extractKnW,
				'Loliquent'                                                     : pfuncs.extractKnW,
				'Pummels Translations'                                          : pfuncs.extractKnW,
				'XCrossJ'                                                       : pfuncs.extractKnW,

				# Broken or not implemented yet
				'Untuned Translation Blog'                                      : pfuncs.extractBase,
				'Bad Translation'                                               : pfuncs.extractBase,
				'HaruPARTY'                                                     : pfuncs.extractBase,
				'Kami Translation'                                              : pfuncs.extractBase,
				'KobatoChanDaiSukiScan'                                         : pfuncs.extractBase,
				'LordofScrubs'                                                  : pfuncs.extractBase,
				'Roasted Tea'                                                   : pfuncs.extractBase,
				'Roxism HQ'                                                     : pfuncs.extractBase,
				'Shin Sekai Yori – From the New World'                          : pfuncs.extractBase,
				'Undecent Translations'                                         : pfuncs.extractBase,
				'ℝeanとann@'                                                     : pfuncs.extractBase,
				'pandafuqtranslations'                                          : pfuncs.extractBase,
				'Prince Revolution!'                                            : pfuncs.extractBase,
				'CtrlAlcalá'                                                    : pfuncs.extractBase,

				'Ducky\'s English Translations'                                 : pfuncs.extractBase,
				'Dreams of Jianghu'                                             : pfuncs.extractBase,
				'Diwasteman'                                                    : pfuncs.extractBase,
				'Dark Translations'                                             : pfuncs.extractBase,
				'Dao Seeker Blog'                                               : pfuncs.extractBase,
				'CookiePasta Translations'                                      : pfuncs.extractBase,
				'Clover\'s Nook'                                                : pfuncs.extractBase,

				'Dewey Night Unrolls'                                           : pfuncs.extractBase,

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
				'Anathema Serial'                                               : pfuncs.extractBase,
				'Andrew9495\'s MTL corner'                                      : pfuncs.extractBase,
				'Anon Empire'                                                   : pfuncs.extractBase,
				'Aori Translations'                                             : pfuncs.extractBase,
				'Aqua Scans'                                                    : pfuncs.extractBase,
				'Archivity'                                                     : pfuncs.extractBase,
				'Azurro 4 Cielo'                                                : pfuncs.extractBase,
				'Bcat00 Translation'                                            : pfuncs.extractBase,
				'Bear Bear Translations'                                        : pfuncs.extractBase,
				'BeRsErk Translations'                                          : pfuncs.extractBase,
				'C Novels 2 C'                                                  : pfuncs.extractBase,
				'Cat Scans'                                                     : pfuncs.extractBase,
				'cavescans.com'                                                 : pfuncs.extractBase,
				'Ceruleonice Translations'                                      : pfuncs.extractBase,
				'Cheddar!'                                                      : pfuncs.extractBase,
				'Chinese BL Translations'                                       : pfuncs.extractBase,
				'Chinese Weaboo Translations'                                   : pfuncs.extractBase,
				'Circle of Shards'                                              : pfuncs.extractBase,
				'Cloud Manor'                                                   : pfuncs.extractBase,
				'Code-Zero\'s Blog'                                             : pfuncs.extractBase,
				'Cosmic Translation'                                            : pfuncs.extractBase,
				'Currently TLing [Bu ni Mi]'                                    : pfuncs.extractBase,
				'Dawning Howls'                                                 : pfuncs.extractBase,
				'Deadly Forgotten Legends'                                      : pfuncs.extractBase,
				'Defan\'s Translations'                                         : pfuncs.extractBase,
				'Descent Subs'                                                  : pfuncs.extractBase,
				'Dorayakiz'                                                     : pfuncs.extractBase,
				'Dream Avenue'                                                  : pfuncs.extractBase,
				'Duran Daru Translation'                                        : pfuncs.extractBase,
				'Durasama'                                                      : pfuncs.extractBase,
				'Dynamis Gaul Light Novel'                                      : pfuncs.extractBase,
				'EC Webnovel'                                                   : pfuncs.extractBase,
				'ELYSION Translation'                                           : pfuncs.extractBase,
				'Emergency Exit\'s Release Blog'                                : pfuncs.extractBase,
				'End Online Novel'                                              : pfuncs.extractBase,
				'EndKun'                                                        : pfuncs.extractBase,
				'Ente38 translations'                                           : pfuncs.extractBase,
				'Epyon Translations'                                            : pfuncs.extractBase,
				'eternalpath.net'                                               : pfuncs.extractBase,
				'Etheria Translations'                                          : pfuncs.extractBase,
				'Eugene Rain'                                                   : pfuncs.extractBase,
				'Eye of Adventure '                                             : pfuncs.extractBase,
				'EZ Translations'                                               : pfuncs.extractBase,
				'Fighting Dreamers Scanlations'                                 : pfuncs.extractBase,
				'Five Star Specialists'                                         : pfuncs.extractBase,
				'Flicker Hero'                                                  : pfuncs.extractBase,
				'Fung Shen'                                                     : pfuncs.extractBase,
				'Fuzion Life'                                                   : pfuncs.extractBase,
				'Gargoyle Web Serial'                                           : pfuncs.extractBase,
				'Goddess! Grant Me a Girlfriend!!'                              : pfuncs.extractBase,
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
				'Joeglen\'s Translation Space'                                  : pfuncs.extractBase,
				'Kahoim Translations'                                           : pfuncs.extractBase,
				'Kedelu'                                                        : pfuncs.extractBase,
				'King Jaahn\'s Subjects'                                        : pfuncs.extractBase,
				'Kisato\'s MLTs'                                                : pfuncs.extractBase,
				'KN Translation'                                                : pfuncs.extractBase,
				'Knokkro Translations'                                          : pfuncs.extractBase,
				'Kore Yori Hachidori'                                           : pfuncs.extractBase,
				'Korean Novel Translations'                                     : pfuncs.extractBase,
				'Krytyk\'s Translations'                                        : pfuncs.extractBase,
				'Kuma Otou'                                                     : pfuncs.extractBase,
				'Kurotsuki Novel'                                               : pfuncs.extractBase,
				'Kyakka Translations'                                           : pfuncs.extractBase,
				'L2M'                                                           : pfuncs.extractBase,
				'Lastvoice Translator'                                          : pfuncs.extractBase,
				'Layzisheep'                                                    : pfuncs.extractBase,
				'Legend of Galactic Heroes Translation Project'                 : pfuncs.extractBase,
				'Light Novel translations'                                      : pfuncs.extractBase,
				'Lil\' Bliss Novels'                                            : pfuncs.extractBase,
				'Linked Translations'                                           : pfuncs.extractBase,
				'Lizard Translations'                                           : pfuncs.extractBase,
				'LMS Machine Translations'                                      : pfuncs.extractBase,
				'Loiterous'                                                     : pfuncs.extractBase,
				'LorCromwell'                                                   : pfuncs.extractBase,
				'Lylis Translations'                                            : pfuncs.extractBase,
				'Machine Sliced Bread'                                          : pfuncs.extractBase,
				'Makina Translations'                                           : pfuncs.extractBase,
				'Mana Tank Magus'                                               : pfuncs.extractBase,
				'Maou na Anoko to murabito a'                                   : pfuncs.extractBase,
				'Martial God Translator'                                        : pfuncs.extractBase,
				'Mecha Mushroom Translations'                                   : pfuncs.extractBase,
				'Midnight Translation Blog'                                     : pfuncs.extractBase,
				'Mnemeaa'                                                       : pfuncs.extractBase,
				'mousou-haven.com'                                              : pfuncs.extractBase,
				'Mystique Translations'                                         : pfuncs.extractBase,
				'n00btranslations.wordpress.com'                                : pfuncs.extractBase,
				'NanoDesu Light Novel Translations'                             : pfuncs.extractBase,
				'National NEET'                                                 : pfuncs.extractBase,
				'NOT Daily Translations'                                        : pfuncs.extractBase,
				'Novels Nao'                                                    : pfuncs.extractBase,
				'Nowhere & Nothing'                                             : pfuncs.extractBase,
				'Nutty is Procrastinating'                                      : pfuncs.extractBase,
				'OK Translation'                                                : pfuncs.extractBase,
				'omatranslations.wordpress.com'                                 : pfuncs.extractBase,
				'Omgitsaray Translations'                                       : pfuncs.extractBase,
				'One Second Spring'                                             : pfuncs.extractBase,
				'Ore ga Heroine in English'                                     : pfuncs.extractBase,
				'Origin Novels'                                                 : pfuncs.extractBase,
				'Otome Revolution'                                              : pfuncs.extractBase,
				'Outspan Foster'                                                : pfuncs.extractBase,
				'Pact Web Serial'                                               : pfuncs.extractBase,
				'Paztok'                                                        : pfuncs.extractBase,
				'Pea Translation'                                               : pfuncs.extractBase,
				'Pielord Translations'                                          : pfuncs.extractBase,
				'Pippi Site'                                                    : pfuncs.extractBase,
				'PlainlyBored'                                                  : pfuncs.extractBase,
				'Polyphonic Story Translation Group'                            : pfuncs.extractBase,
				'Popsiclete'                                                    : pfuncs.extractBase,
				'Project Accelerator'                                           : pfuncs.extractBase,
				'Pumpkin Translations'                                          : pfuncs.extractBase,
				'Quality ★ Mistranslations'                                    : pfuncs.extractBase,
				'Rainbow Translations'                                          : pfuncs.extractBase,
				'Raising Angels & Defection'                                    : pfuncs.extractBase,
				'Rebirth Online World'                                          : pfuncs.extractBase,
				'Red Dragon Translations'                                       : pfuncs.extractBase,
				'Reddy Creations'                                               : pfuncs.extractBase,
				'Reigokai: Isekai Translations'                                 : pfuncs.extractBase,
				'Reject Hero'                                                   : pfuncs.extractBase,
				'Require: Cookie'                                               : pfuncs.extractBase,
				'Romantic Dreamer\'s Sanctuary'                                 : pfuncs.extractBase,
				'Rosyfantasy - Always Dreaming'                                 : pfuncs.extractBase,
				'Rumanshi\'s Lair'                                              : pfuncs.extractBase,
				'Rumor\'s Block'                                                : pfuncs.extractBase,
				'Saber Translations'                                            : pfuncs.extractBase,
				'Sauri\'s TL Blog'                                              : pfuncs.extractBase,
				'SETSUNA86BLOG'                                                 : pfuncs.extractBase,
				'Sherma Translations'                                           : pfuncs.extractBase,
				'Shinsori Translations'                                         : pfuncs.extractBase,
				'Shokyuu Translations'                                          : pfuncs.extractBase,
				'Silva\'s Library'                                              : pfuncs.extractBase,
				'Silver Butterfly'                                              : pfuncs.extractBase,
				'Sins of the Fathers'                                           : pfuncs.extractBase,
				'Slime Lv1'                                                     : pfuncs.extractBase,
				'Snow & Dust'                                                   : pfuncs.extractBase,
				'Soaring Translations'                                          : pfuncs.extractBase,
				'soaringtranslations.wordpress.com'                             : pfuncs.extractBase,
				'solitarytranslation.wordpress.com'                             : pfuncs.extractBase,
				'Sora Translationsblog'                                         : pfuncs.extractBase,
				'Stellar Transformation Con.'                                   : pfuncs.extractBase,
				'STL Translations'                                              : pfuncs.extractBase,
				'Stone Burners'                                                 : pfuncs.extractBase,
				'Subudai11'                                                     : pfuncs.extractBase,
				'Sun Shower Fields'                                             : pfuncs.extractBase,
				'Super Potato Translations'                                     : pfuncs.extractBase,
				'Symbiote'                                                      : pfuncs.extractBase,
				'tap-trans » tappity tappity tap.'                              : pfuncs.extractBase,
				'Terminus Translation'                                          : pfuncs.extractBase,
				'The Mustang Translator'                                        : pfuncs.extractBase,
				'The Named'                                                     : pfuncs.extractBase,
				'The Sphere'                                                    : pfuncs.extractBase,
				'The Tales of Paul Twister'                                     : pfuncs.extractBase,
				'TheDefend Translations'                                        : pfuncs.extractBase,
				'Tieshaunn'                                                     : pfuncs.extractBase,
				'tiffybook.com'                                                 : pfuncs.extractBase,
				'Tofubyu'                                                       : pfuncs.extractBase,
				'Totally Insane Tranlation'                                     : pfuncs.extractBase,
				'Translation Raven'                                             : pfuncs.extractBase,
				'Translation Treasure Box'                                      : pfuncs.extractBase,
				'Translations From Outer Space'                                 : pfuncs.extractBase,
				'Trungt Nguyen 123'                                             : pfuncs.extractBase,
				'Tsukigomori'                                                   : pfuncs.extractBase,
				'Tumble Into Fantasy'                                           : pfuncs.extractBase,
				'Tus-Trans'                                                     : pfuncs.extractBase,
				'Twisted Cogs'                                                  : pfuncs.extractBase,
				'U Donate We Translate'                                         : pfuncs.extractBase,
				'Ultimate Arcane'                                               : pfuncs.extractBase,
				'Unlimited Story Works'                                         : pfuncs.extractBase,
				'Useless no 4'                                                  : pfuncs.extractBase,
				'Village Translations'                                          : pfuncs.extractBase,
				'walkthejianghu.wordpress.com'                                  : pfuncs.extractBase,
				'Wat Da Meow'                                                   : pfuncs.extractBase,
				'Watermelon Helmets'                                            : pfuncs.extractBase,
				'Weaving stories and building castles in the clouds'            : pfuncs.extractBase,
				'Wele Translation'                                              : pfuncs.extractBase,
				'When The Hunting Party Came'                                   : pfuncs.extractBase,
				'Whimsical Land'                                                : pfuncs.extractBase,
				'White Tiger Translations'                                      : pfuncs.extractBase,
				'Wolfie Translation'                                            : pfuncs.extractBase,
				'Word of Craft'                                                 : pfuncs.extractBase,
				'World of Summie'                                               : pfuncs.extractBase,
				'Worm - A Complete Web Serial'                                  : pfuncs.extractBase,
				'Wuxiwish'                                                      : pfuncs.extractBase,
				'www.pridesfamiliarsmaidens.com'                                : pfuncs.extractBase,
				'www.soltarination.org'                                         : pfuncs.extractBase,
				'Xant & Minions'                                                : pfuncs.extractBase,
				'xantbos.wordpress.com'                                         : pfuncs.extractBase,
				'Yet Another Translation Site'                                  : pfuncs.extractBase,
				'Yi Yue Translation'                                            : pfuncs.extractBase,
				'youtsubasilver\'s Blog'                                        : pfuncs.extractBase,
				'Zen Translations'                                              : pfuncs.extractBase,
				'~Taffy Translations~'                                          : pfuncs.extractBase,
				'ヾ(。￣□￣)ﾂ'                                                    : pfuncs.extractBase,
				'一期一会, 万歳!'                                                : pfuncs.extractBase,
				'睡眠中毒'                                                       : pfuncs.extractBase,
				'輝く世界'                                                        : pfuncs.extractBase,


		}



		if item['srcname'] in funcMap:
			ret = funcMap[item['srcname']](item)
		else:
			print("No filter found?")


		if (flags.RSS_DEBUG or self.dbg_print) and self.write_debug and not ret:
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if vol or chp or frag and not flags.RSS_DEBUG:

				with open('rss_filter_misses-1.txt', "a") as fp:

					write_items = [
						("SourceName: ", item['srcname']),
						("Title: ", item['title']),
						("Tags: ", item['tags']),
						("Vol: ", vol),
						("Chp: ", chp),
						("Frag: ", frag),
						("Postfix: ", postfix),
						("Feed URL: ", item['linkUrl']),
						("GUID: ", item['guid']),
					]

					# fp.write("\n==============================\n")
					# fp.write("Feed URL: '%s', guid: '%s'" % (item['linkUrl'], item['guid']))
					# fp.write("'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'\n" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix, item['linkUrl']))
					for name, val in write_items:
						fp.write("%s '%s', " % (name, val))
					fp.write("\n")

		if self.dbg_print or flags.RSS_DEBUG:
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if not ret and (vol or chp or frag):
				print("Missed: '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))
			elif ret:
				pass
				print("OK! '%s', V:'%s', C:'%s', '%s', '%s', '%s'" % (ret['srcname'], ret['vol'], ret['chp'], ret['postfix'], ret['series'], item['title']))
			else:
				pass
				print("Wat: '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix, item['linkUrl']))

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
			# print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return

		netloc = urllib.parse.urlparse(feedDat['linkUrl']).netloc

		# print("ProcessFeedData! ", netloc)
		if not WebMirror.rules.netloc_send_feed(netloc):
			# print("Not sending data for netloc: ", netloc)
			return

		nicename = feedNameLut.getNiceName(feedDat['linkUrl'])
		if not nicename:
			nicename = netloc


		# if not nicename in self.names:
		# 	self.names.add(nicename)
		# 	# print(nicename)

		feedDat['srcname'] = nicename


		if tx_raw:
			raw = self.getRawFeedMessage(feedDat)
			if raw:
				self.amqp_put_item(raw)

		if tx_parse:
			new = self.getProcessedReleaseInfo(feedDat)
			if new:
				self.amqp_put_item(new)

