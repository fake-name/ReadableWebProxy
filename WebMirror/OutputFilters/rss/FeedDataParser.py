
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import json
import traceback
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut


import WebMirror.OutputFilters.rss.ParserFuncs_a_g     as pfuncs_a_g
import WebMirror.OutputFilters.rss.ParserFuncs_h_n     as pfuncs_h_n
import WebMirror.OutputFilters.rss.ParserFuncs_o_u     as pfuncs_o_u
import WebMirror.OutputFilters.rss.ParserFuncs_v_other as pfuncs_v_other
import WebMirror.OutputFilters.rss.ParserFuncs_stub    as pfuncs_stub

from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import WebMirror.OutputFilters.FilterBase
import WebMirror.rules
import flags
import common.global_constants



RSS_PARSE_FUNCTION_MAP = {



				"'Ball'-Kicking Gang Boss"                                             : pfuncs_a_g.extractBallKickingGangBoss,
				"Ankydon's Lair"                                                       : pfuncs_a_g.extractAnkydonsLair,
				"Cautr's"                                                              : pfuncs_a_g.extractCautrs,
				"DOW's Translations"                                                   : pfuncs_a_g.extractDOWsTranslations,
				"Dreamless Window's translation"                                       : pfuncs_a_g.extractDreamlessWindowsTranslation,
				"Evida's Indo Romance"                                                 : pfuncs_a_g.extractEvidasIndoRomance,
				"Hecate's Corner"                                                      : pfuncs_h_n.extractHecatesCorner,
				"Hirika's MTs"                                                         : pfuncs_h_n.extractHirikasMTs,
				"Hon'yaku"                                                             : pfuncs_h_n.extractHonyaku,
				"Hugs & Love"                                                          : pfuncs_h_n.extractHugsAndLove,
				"Ian's Corner"                                                         : pfuncs_h_n.extractIansCorner,
				"kha'sinTH"                                                            : pfuncs_h_n.extractKhasinTH,
				"Monkoto's Translations"                                               : pfuncs_h_n.extractMonkotosTranslations,
				"My Brain's Art"                                                       : pfuncs_h_n.extractMyBrainsArt,
				"Pandora's Book"                                                       : pfuncs_o_u.extractPandorasBook,
				"ProfessionalGameThrower's Translation"                                : pfuncs_o_u.extractProfessionalGameThrowersTranslations,
				"Rui's Translations"                                                   : pfuncs_o_u.extractRuisTranslations,
				"Sarah's lil Novels Corner"                                            : pfuncs_o_u.extractSarahslilNovelsCorner,
				"Silavin's Translations"                                               : pfuncs_o_u.extractSilavinsTranslations,
				"Snail's Pace"                                                         : pfuncs_o_u.extractSnailsPace,
				"WizThief's Novels"                                                    : pfuncs_v_other.extractWizThiefsNovels,
				"Xiaowen206's Blog"                                                    : pfuncs_v_other.extractXiaowen206sBlog,
				"Yuanshu's Cave"                                                       : pfuncs_v_other.extractYuanshusCave,
				"Zxzxzx's blog"                                                        : pfuncs_v_other.extractZxzxzxsBlog,
				'(NanoDesu) - Aldnoah Zero'                                            : pfuncs_h_n.extractNanodesuAldnoahZero,
				'(NanoDesu) - Amagi Brilliant Park '                                   : pfuncs_h_n.extractNanoDesuAmagiBrilliantPark,
				'(NanoDesu) - Biblia Koshodou no Jiken Techou'                         : pfuncs_h_n.extractNanodesuBibliaKoshodouNoJikenTechou,
				'(NanoDesu) - Fate/Apocrypha'                                          : pfuncs_h_n.extractNanoDesuFateApocrypha,
				'(NanoDesu) - Fuyuu Gakuen no Alice and Shirley'                       : pfuncs_h_n.extractNanoDesuFuyuuGakuennoAliceandShirley,
				'(NanoDesu) - Gekka no Utahime to Magi no Ou'                          : pfuncs_h_n.extractNanoDesuGekkanoUtahimetoMaginoOu,
				'(NanoDesu) - GJ-Bu'                                                   : pfuncs_h_n.extractNanoDesuGJBu,
				'(NanoDesu) - Hai to Gensou no Grimgal'                                : pfuncs_h_n.extractNanoDesuHaitoGensounoGrimgal,
				'(NanoDesu) - Hai to Gensou no Grimgar'                                : pfuncs_h_n.extractNanodesuHaiToGensouNoGrimgar,
				'(NanoDesu) - Hentai Ouji to Warawanai Neko'                           : pfuncs_h_n.extractNanoDesuHentaiOujitoWarawanaiNeko,
				'(NanoDesu) - Iriya no Sora, UFO no Natsu'                             : pfuncs_h_n.extractNanodesuIriyaNoSoraUfoNoNatsu,
				'(NanoDesu) - Kono Sekai ga Game Dato Ore Dake ga Shitteiru'           : pfuncs_h_n.extractNanoDesuKonoSekaigaGameDatoOreDakegaShitteiru,
				'(NanoDesu) - Kore wa Zombie Desu ka?'                                 : pfuncs_h_n.extractNanoDesuKorewaZombieDesuka,
				'(NanoDesu) - Kurenai'                                                 : pfuncs_h_n.extractNanoDesuKurenai,
				'(NanoDesu) - Love★You'                                                : pfuncs_h_n.extractNanoDesuLoveYou,
				'(NanoDesu) - Maoyuu Maou Yuusha'                                      : pfuncs_h_n.extractNanoDesuMaoyuuMaouYuusha,
				'(NanoDesu) - Mayo Chiki'                                              : pfuncs_h_n.extractNanoDesuMayoChiki,
				'(NanoDesu) - Ojamajo Doremi'                                          : pfuncs_h_n.extractNanoDesuOjamajoDoremi,
				'(NanoDesu) - Oreimo'                                                  : pfuncs_h_n.extractNanoDesuOreimo,
				'(NanoDesu) - Rokka no Yuusha'                                         : pfuncs_h_n.extractNanoDesuRokkanoYuusha,
				'(NanoDesu) - Saenai Heroine no Sodatekata'                            : pfuncs_h_n.extractNanoDesuSaenaiHeroinenoSodatekata,
				'(NanoDesu) - Sasami-San@Ganbaranai'                                   : pfuncs_h_n.extractNanoDesuSasamiSanGanbaranai,
				'(NanoDesu) - Seitokai no Ichizon'                                     : pfuncs_h_n.extractNanoDesuSeitokainoIchizon,
				'(NanoDesu) - Sky World'                                               : pfuncs_h_n.extractNanoDesuSkyWorld,
				'(NanoDesu) - The Fire Girl'                                           : pfuncs_h_n.extractNanodesuTheFireGirl,
				'(NanoDesu) - Vermillion'                                              : pfuncs_h_n.extractNanodesuVermillion,
				'(NanoDesu) - Yahari Ore no Seishun Love Come wa Machigatteiru'        : pfuncs_h_n.extractNanoDesuYahariOrenoSeishunLoveComewaMachigatteiru,
				'(NanoDesu) - Zero Kara Hajimeru Mahou no Sho!'                        : pfuncs_h_n.extractNanodesuZeroKaraHajimeruMahouNoSho,
				'(NanoDesuCN) - Magical GF'                                            : pfuncs_h_n.extractNanodesucnMagicalGf,
				'-Sloth-'                                                              : pfuncs_o_u.extractSloth,
				'/'                                                                    : pfuncs_a_g.extractForwardSlash,
				'12 Superlatives'                                                      : pfuncs_v_other.extract12Superlatives,
				'1HP'                                                                  : pfuncs_v_other.extract1HP,
				'50% Translations'                                                     : pfuncs_v_other.extract50Translations,
				'7 Days Trial'                                                         : pfuncs_v_other.extract7DaysTrial,
				'77 Novel'                                                             : pfuncs_v_other.extract77Novel,
				'87 Percent Translation'                                               : pfuncs_v_other.extract87Percent,
				'[G.O] Chronicles'                                                     : pfuncs_a_g.extractGOChronicles,
				'[nakulas]'                                                            : pfuncs_h_n.extractNakulas,
				'A Cup of Memory'                                                      : pfuncs_a_g.extractACupofMemory,
				'A fish once said this to me'                                          : pfuncs_a_g.extractDarkFish,
				'A Grey World'                                                         : pfuncs_a_g.extractAGreyWorld,
				'A Little Mirage Translation'                                          : pfuncs_a_g.extractALittleMirageTranslation,
				'A Pearly View'                                                        : pfuncs_a_g.extractAPearlyView,
				'A Place Of Legends'                                                   : pfuncs_o_u.extractPlaceOfLegends,
				'A Purple Blob'                                                        : pfuncs_a_g.extractAPurpleBlob,
				'A Translation of the Bu Ni Mi Light Novel '                           : pfuncs_a_g.extractATranslationOfTheBuNiMiLightNovel,
				'A Translator\'s Journey'                                              : pfuncs_a_g.extractATranslatorSJourney,
				'A Translator\'s Ramblings'                                            : pfuncs_a_g.extractATranslatorsRamblings,
				'A traveler\'s translations.'                                          : pfuncs_a_g.extractATravelersTranslations,
				'A0132'                                                                : pfuncs_a_g.extractA0132,
				'ABCpwip'                                                              : pfuncs_a_g.extractABCpwip,
				'Absurd Translation'                                                   : pfuncs_a_g.extractAbsurdTranslation,
				'Adamantine Dragon in the Crystal World'                               : pfuncs_a_g.extractAdamantineDragonintheCrystalWorld,
				'Adarshan no Hanayome'                                                 : pfuncs_a_g.extractAdarshanNoHanayome,
				'AeRoSoL31'                                                            : pfuncs_a_g.extractAeRoSoL31,
				'AFlappyTeddyBird'                                                     : pfuncs_a_g.extractAFlappyTeddyBird,
				'After;Translations'                                                   : pfuncs_a_g.extractAfterTranslations,
				'Agrypnia Scans'                                                       : pfuncs_a_g.extractAgrypniaScans,
				'Ai Hrist Dream Translations'                                          : pfuncs_a_g.extractAiHristDreamTranslations,
				'Ainushi Translations 愛主の翻訳'                                           : pfuncs_a_g.extractAinushiTranslations愛主の翻訳,
				'AJRG'                                                                 : pfuncs_a_g.extractAJRG,
				'Albert Kenoreijou'                                                    : pfuncs_a_g.extractAlbertKenoreijou,
				'Alchyr does things'                                                   : pfuncs_a_g.extractAlchyrdoesthings,
				'Alcsel Translations'                                                  : pfuncs_a_g.extractAlcsel,
				'Alice Translations'                                                   : pfuncs_a_g.extractAliceTranslations,
				'AliceMTL'                                                             : pfuncs_a_g.extractAlicemtl,
				'alicetranslations.wordpress.com'                                      : pfuncs_a_g.extractAlicetranslations,
				'All\'s Fair In Love & War'                                            : pfuncs_a_g.extractAllsFairInLoveWar,
				'Almighty Athlete'                                                     : pfuncs_a_g.extractAlmightyAthlete,
				'Alpen Glow Translations'                                              : pfuncs_a_g.extractAlpenGlowTranslations,
				'Alternative Projects'                                                 : pfuncs_a_g.extractAlternativeProjects,
				'Altoroc Translations'                                                 : pfuncs_a_g.extractAltorocTranslations,
				'Alyschu & Co'                                                         : pfuncs_a_g.extractAlyschuCo,
				'American Faux'                                                        : pfuncs_a_g.extractAmericanFaux,
				'Amery Edge'                                                           : pfuncs_a_g.extractAmeryEdge,
				'Ananas Parfait'                                                       : pfuncs_a_g.extractAnanasParfait,
				'Anathema Serial'                                                      : pfuncs_a_g.extractAnathema,
				'Andrew9495\'s MTL corner'                                             : pfuncs_a_g.extractAndrew9495,
				'Andromeda & Boul'                                                     : pfuncs_a_g.extractAndromedaBoul,
				'Anime, manga, translations'                                           : pfuncs_a_g.extractAnimeMangaTranslations,
				'Anime, Manga, Translations'                                           : pfuncs_a_g.extractAnimeMangaTranslations,
				'Anime-Expressions'                                                    : pfuncs_a_g.extractAnimeExpressions,
				'Ankou Translations'                                                   : pfuncs_a_g.extractAnkouTranslations,
				'Anne And Cindy'                                                       : pfuncs_a_g.extractAnneAndCindy,
				'Anon Empire'                                                          : pfuncs_a_g.extractAnonEmpire,
				'Another Parallel World'                                               : pfuncs_a_g.extractAnotherParallelWorld,
				'Another World Translations'                                           : pfuncs_a_g.extractAnotherWorldTranslations,
				'Antheor'                                                              : pfuncs_a_g.extractAntheor,
				'Aoitenshi Manga Scanlation'                                           : pfuncs_a_g.extractAoitenshiMangaScanlation,
				'Aori Translations'                                                    : pfuncs_a_g.extractAoriTranslations,
				'Apollo Translations'                                                  : pfuncs_a_g.extractApolloTranslations,
				'Aqua Scans'                                                           : pfuncs_a_g.extractAquaScans,
				'Aquarilas\' Scenario'                                                 : pfuncs_a_g.extractAquarilasScenario,
				'Aran Translations'                                                    : pfuncs_a_g.extractAranTranslations,
				'Arc\'s Translations'                                                  : pfuncs_a_g.extractArcSTranslations,
				'Archivity'                                                            : pfuncs_a_g.extractArchivity,
				'Ares Novels'                                                          : pfuncs_a_g.extractAresNovels,
				'Ark Machine Translations'                                             : pfuncs_a_g.extractArkMachineTranslations,
				'Arousing Imouto'                                                      : pfuncs_a_g.extractArousingImouto,
				'Arteg the Bear'                                                       : pfuncs_a_g.extractArtegTheBear,
				'asd398'                                                               : pfuncs_a_g.extractAsd398,
				'AsherahBlue\'s Notebook'                                              : pfuncs_a_g.extractAsherahBlue,
				'Asthmatic Spider Translations'                                        : pfuncs_a_g.extractAsthmaticSpiderTranslations,
				'Asura Tales'                                                          : pfuncs_a_g.extractAsuraTales,
				'Asylum Translations'                                                  : pfuncs_a_g.extractAsylumTranslations,
				'Aten Translations'                                                    : pfuncs_a_g.extractAtenTranslations,
				'Auantum Novel'                                                        : pfuncs_a_g.extractAuantumNovel,
				'Avaritia-kun'                                                         : pfuncs_a_g.extractAvaritiakun,
				'Avert Translations'                                                   : pfuncs_a_g.extractAvert,
				'Avert Translations~'                                                  : pfuncs_a_g.extractAvertTranslations,
				'Ayax World'                                                           : pfuncs_a_g.extractAyaxWorld,
				'Azure Sky Translation'                                                : pfuncs_a_g.extractAzureSky,
				'Azurro 4 Cielo'                                                       : pfuncs_a_g.extractAzurro,
				'Bad Translation'                                                      : pfuncs_a_g.extractBadTranslation,
				'Baka Dogeza Translation'                                              : pfuncs_a_g.extractBakaDogeza,
				'Baka Pervert'                                                         : pfuncs_a_g.extractBakaPervert,
				'Baka-Tsuki e-pub Generator'                                           : pfuncs_a_g.extractBakaTsukiEPubGenerator,
				'Baka-Tsuki'                                                           : pfuncs_a_g.extractBakaTsuki,
				'Bakahou'                                                              : pfuncs_a_g.extractBakahou,
				'Bananas'                                                              : pfuncs_a_g.extractBananas,
				'Bayabusco Translation'                                                : pfuncs_a_g.extractBayabuscoTranslation,
				'Bcat00 Translation'                                                   : pfuncs_a_g.extractBcat00,
				'Bear Bear Translations'                                               : pfuncs_a_g.extractBearBearTranslations,
				'Beehugger'                                                            : pfuncs_a_g.extractBeehugger,
				'Beer Happy Translations'                                              : pfuncs_a_g.extractBeerHappyTranslations,
				'Berseker Translations'                                                : pfuncs_a_g.extractBersekerTranslations,
				'BeRsErk Translations'                                                 : pfuncs_a_g.extractBeRsErkTranslations,
				'Bijinsans'                                                            : pfuncs_a_g.extractBijinsans,
				'Binggo&Corp'                                                          : pfuncs_a_g.extractBinggoCorp,
				'Binhjamin'                                                            : pfuncs_a_g.extractBinhjamin,
				'Bionicark Translations'                                               : pfuncs_a_g.extractBionicarkTranslations,
				'Birdy Translations'                                                   : pfuncs_a_g.extractBirdyTranslations,
				'BL Drama Diary'                                                       : pfuncs_a_g.extractBlDramaDiary,
				'BL Novel Obsession'                                                   : pfuncs_a_g.extractBLNovelObsession,
				'Blade of Hearts'                                                      : pfuncs_a_g.extractBladeOfHearts,
				'Blastron Does Some Things'                                            : pfuncs_a_g.extractBlastronDoesSomeThings,
				'Blazing Translations'                                                 : pfuncs_h_n.extractKnW,
				'Blublub'                                                              : pfuncs_a_g.extractBlublub,
				'Blue Phoenix'                                                         : pfuncs_a_g.extractBluePhoenix,
				'Blue Silver Translations'                                             : pfuncs_a_g.extractBlueSilverTranslations,
				'Bluefire Translations'                                                : pfuncs_a_g.extractBluefireTranslations,
				'Books Movies and Beyond'                                              : pfuncs_a_g.extractBooksMoviesAndBeyond,
				'Bo~'                                                                  : pfuncs_a_g.extractBo,
				'Bruin Translation'                                                    : pfuncs_a_g.extractBruinTranslation,
				'Bu Bu Jing Xin Translation'                                           : pfuncs_a_g.extractBuBuJingXinTrans,
				'Burei Dan Works'                                                      : pfuncs_a_g.extractBureiDan,
				'C Novels 2 C'                                                         : pfuncs_a_g.extractCNovels2C,
				'C-Novel Tranlations…'                                                 : pfuncs_a_g.extractCNovelTranlations,
				'C.E. Light Novel Translations'                                        : pfuncs_a_g.extractCeLn,
				'Caged Bramblings In A Pavilion'                                       : pfuncs_a_g.extractCagedBramblingsInAPavilion,
				'Calico x Tabby'                                                       : pfuncs_a_g.extractCalicoxTabby,
				'CapsUsingShift Tl'                                                    : pfuncs_h_n.extractKnW,
				'Cas Project Site'                                                     : pfuncs_a_g.extractCasProjectSite,
				'Cat Scans'                                                            : pfuncs_a_g.extractCatScans,
				'CaveScans'                                                            : pfuncs_a_g.extractCaveScans,
				'cavescans.com'                                                        : pfuncs_a_g.extractCaveScans,
				'Ceruleonice Translations'                                             : pfuncs_a_g.extractCeruleonice,
				'Chaos Words'                                                          : pfuncs_a_g.extractChaosWords,
				'Chaotic Neutral'                                                      : pfuncs_a_g.extractChaoticNeutral,
				'Chaotic Sword Translations'                                           : pfuncs_a_g.extractChaoticSwordTranslations,
				'Chaotic Translations'                                                 : pfuncs_a_g.extractChaoticTranslations,
				'Chauffeur Translations'                                               : pfuncs_a_g.extractChauffeurTranslations,
				'Cheddar!'                                                             : pfuncs_a_g.extractCheddar,
				'Chilly Territory'                                                     : pfuncs_a_g.extractChillyTerritory,
				'Chimp\'s MTL Spot'                                                    : pfuncs_a_g.extractChimpsMTLSpot,
				'China Light Novel'                                                    : pfuncs_a_g.extractChinaLightNovel,
				'China Novel.net'                                                      : pfuncs_a_g.extractChinaNovelNet,
				'Chinese BL Translations'                                              : pfuncs_a_g.extractChineseBLTranslations,
				'Chinese Novel Translated'                                             : pfuncs_a_g.extractChineseNovelTranslated,
				'Chinese Weaboo Translations'                                          : pfuncs_a_g.extractChineseWeabooTranslations,
				'ChocolateCosmos Translations'                                         : pfuncs_a_g.extractChocolateCosmosTranslations,
				'Chongmei Translations'                                                : pfuncs_a_g.extractChongmeiTranslations,
				'Choyce.club'                                                          : pfuncs_a_g.extractChoyceClub,
				'Chrona Zero'                                                          : pfuncs_a_g.extractChronaZero,
				'Chronicles of Gaia'                                                   : pfuncs_a_g.extractChroniclesofGaia,
				'Chronon Translations'                                                 : pfuncs_a_g.extractChrononTranslations,
				'ChubbyCheeks'                                                         : pfuncs_a_g.extractChubbyCheeks,
				'Ciaran Hillock'                                                       : pfuncs_a_g.extractCiaranHillock,
				'Circa Translations'                                                   : pfuncs_a_g.extractCircaTranslations,
				'Circle of Shards'                                                     : pfuncs_a_g.extractCircleofShards,
				'Circus Translations'                                                  : pfuncs_a_g.extractCircusTranslations,
				'Clesesia Blogspot~'                                                   : pfuncs_a_g.extractClesesiaBlogspot,
				'Clicky Click Translation'                                             : pfuncs_a_g.extractClicky,
				'Cloud Manor'                                                          : pfuncs_a_g.extractCloudManor,
				'Cloud Translations'                                                   : pfuncs_a_g.extractCloudTranslations,
				'Clover\'s Nook'                                                       : pfuncs_a_g.extractCloversNook,
				'Clôture of Yellow'                                                    : pfuncs_a_g.extractClôtureOfYellow,
				'Cnovel <3'                                                            : pfuncs_a_g.extractCnovel3,
				'Cocobees'                                                             : pfuncs_a_g.extractCocobees,
				'Code-Zero\'s Blog'                                                    : pfuncs_a_g.extractCodeZerosBlog,
				'Collection.'                                                          : pfuncs_a_g.extractCollection,
				'Confessions of a Drama Addict'                                        : pfuncs_a_g.extractConfessionsOfADramaAddict,
				'CookiePasta Translations'                                             : pfuncs_a_g.extractCookiePasta,
				'CookiePasta'                                                          : pfuncs_a_g.extractCookiePasta,
				'Cosmic Translation'                                                   : pfuncs_a_g.extractCosmicTranslation,
				'Crack of Dawn Translations'                                           : pfuncs_a_g.extractCrackofDawnTranslations,
				'Crappy Machine Translation'                                           : pfuncs_a_g.extractCrappyMachineTranslation,
				'Crazy for HE Novels'                                                  : pfuncs_a_g.extractCrazyForHENovels,
				'Cream Savers'                                                         : pfuncs_a_g.extractCreamSavers,
				'Creepy and Evil Translations'                                         : pfuncs_a_g.extractCreepyAndEvilTranslations,
				'CrystalRainDescends'                                                  : pfuncs_a_g.extractCrystalRainDescends,
				'CtrlAlcalá'                                                           : pfuncs_a_g.extractCtrlAlcala,
				'Currently TLing [Bu ni Mi]'                                           : pfuncs_a_g.extractCurrentlyTLingBuniMi,
				'DadIsHero Fan Translations'                                           : pfuncs_a_g.extractDadIsHeroFanTranslations,
				'Daikyun Translations'                                                 : pfuncs_a_g.extractDaikyunTranslations,
				'Daily Dose Novels'                                                    : pfuncs_a_g.extractDailyDoseNovels,
				'Daily-Dallying'                                                       : pfuncs_a_g.extractDailyDallying,
				'Dandelion Trail'                                                      : pfuncs_a_g.extractDandelionTrail,
				'Dao Seeker Blog'                                                      : pfuncs_a_g.extractDaoSeekerBlog,
				'Dark Translations'                                                    : pfuncs_a_g.extractDarkTranslations,
				'Datebayo Blog'                                                        : pfuncs_a_g.extractDatebayoBlog,
				'Daupao'                                                               : pfuncs_a_g.extractDaupao,
				'Dawning Howls'                                                        : pfuncs_a_g.extractDawningHowls,
				'Daydream Translations'                                                : pfuncs_a_g.extractDaydreamTranslations,
				'Deadly Forgotten Legends'                                             : pfuncs_a_g.extractDeadlyForgottenLegends,
				'Dearest Fairy'                                                        : pfuncs_a_g.extractDearestFairy,
				'Death Knight'                                                         : pfuncs_a_g.extractDeathKnight,
				'Death Might\'s Translating Legion'                                    : pfuncs_a_g.extractDeathMightSTranslatingLegion,
				'Death, taxes, and fandom.'                                            : pfuncs_a_g.extractDeathTaxesAndFandom,
				'Deep Azure Sky'                                                       : pfuncs_a_g.extractDeepAzureSky,
				'Defan\'s Translations'                                                : pfuncs_a_g.extractDefansTranslations,
				'Defiring'                                                             : pfuncs_a_g.extractDefiring,
				'Dekinai Diary'                                                        : pfuncs_a_g.extractDekinaiDiary,
				'Delicious Translations'                                               : pfuncs_a_g.extractDeliciousTranslations,
				'Demerith Translation'                                                 : pfuncs_a_g.extractDemerithTranslation,
				'Demon Scorpion Translations'                                          : pfuncs_a_g.extractDemonScorpionTranslations,
				'Demon Translations'                                                   : pfuncs_a_g.extractDemonTranslations,
				'Descent Subs'                                                         : pfuncs_a_g.extractDescentSubs,
				'devildante777\'s Blog'                                                : pfuncs_a_g.extractDevildante777SBlog,
				'Dewey Night Unrolls'                                                  : pfuncs_a_g.extractDeweyNightUnrolls,
				'DHH Translations'                                                     : pfuncs_a_g.extractDHHTranslations,
				'Disappointing Translations'                                           : pfuncs_a_g.extractDisappointingTranslations,
				'Distracted Chinese'                                                   : pfuncs_a_g.extractDistractedChinese,
				'Distracted Translations'                                              : pfuncs_a_g.extractDistractedTranslations,
				'Diwasteman'                                                           : pfuncs_a_g.extractDiwasteman,
				'DokuHana Translations'                                                : pfuncs_a_g.extractDokuHanaTranslations,
				'Dorayakiz'                                                            : pfuncs_a_g.extractDorayakiz,
				'Doushi no Jikan scanlations'                                          : pfuncs_a_g.extractDoushiNoJikanScanlations,
				'DragomirCM'                                                           : pfuncs_a_g.extractDragomirCM,
				'Dragon MT'                                                            : pfuncs_a_g.extractDragonMT,
				'Drake Translations'                                                   : pfuncs_a_g.extractDrakeTranslations,
				'Dramas, Books & Tea'                                                  : pfuncs_a_g.extractDramasBooksTea,
				'Dreadful Decoding'                                                    : pfuncs_a_g.extractDreadfulDecoding,
				'Dream Avenue'                                                         : pfuncs_a_g.extractDreamAvenue,
				'Dreams of Jianghu'                                                    : pfuncs_a_g.extractDreamsOfJianghu,
				'Ducky\'s English Translations'                                        : pfuncs_a_g.extractDuckysEnglishTranslations,
				'Duran Daru Translation'                                               : pfuncs_a_g.extractDuranDaruTranslation,
				'Durasama'                                                             : pfuncs_a_g.extractDurasama,
				'Dusk Tales'                                                           : pfuncs_a_g.extractDuskTales,
				'Dust to Rust'                                                         : pfuncs_a_g.extractDustToRust,
				'Dwrf TL'                                                              : pfuncs_a_g.extractDwrfTL,
				'Dynamis Gaul Light Novel'                                             : pfuncs_a_g.extractDynamisGaul,
				'Dysry Summaries'                                                      : pfuncs_a_g.extractDysrySummaries,
				'E. Zani Fiction'                                                      : pfuncs_a_g.extractEZaniFiction,
				'Eastern Fantasy'                                                      : pfuncs_a_g.extractEasternFantasy,
				'EC Webnovel'                                                          : pfuncs_a_g.extractECWebnovel,
				'EccentricTranslations'                                                : pfuncs_a_g.extractEccentricTranslations,
				'EG-Smart-Translation'                                                 : pfuncs_a_g.extractEGSmartTranslation,
				'EGSN Blog'                                                            : pfuncs_a_g.extractEGSNBlog,
				'Elemental Cobalt'                                                     : pfuncs_a_g.extractElementalCobalt,
				'Elli Phantomhive♥'                                                    : pfuncs_a_g.extractElliPhantomhive,
				'Ellionora Translation'                                                : pfuncs_a_g.extractEllionoraTranslation,
				'ELYSION Translation'                                                  : pfuncs_a_g.extractELYSIONTranslation,
				'Emergency Exit\'s Release Blog'                                       : pfuncs_a_g.extractEmergencyExitsReleaseBlog,
				'Empty Boundaries'                                                     : pfuncs_a_g.extractEmptyBoundaries,
				'Emruyshit Translations'                                               : pfuncs_a_g.extractEmruyshitTranslations,
				'En Xiao'                                                              : pfuncs_a_g.extractEnXiao,
				'End of Doom MTL'                                                      : pfuncs_a_g.extractEndofDoomMTL,
				'End of the days42'                                                    : pfuncs_a_g.extractEndofthedays42,
				'End Online Novel'                                                     : pfuncs_a_g.extractEndOnline,
				'Endeta'                                                               : pfuncs_a_g.extractEndeta,
				'EndKun'                                                               : pfuncs_a_g.extractEndKun,
				'EndlessFantasy Translations'                                          : pfuncs_a_g.extractEndlessfantasyTranslations,
				'Enlate'                                                               : pfuncs_a_g.extractEnlate,
				'Ensig\'s Writings'                                                    : pfuncs_a_g.extractEnsigsWritings,
				'Ensj Translations'                                                    : pfuncs_a_g.extractEnsjTranslations,
				'Ente38 translations'                                                  : pfuncs_a_g.extractEnte38translations,
				'EnTruce Translations'                                                 : pfuncs_a_g.extractEnTruceTranslations,
				'Epithetic'                                                            : pfuncs_a_g.extractEpithetic,
				'Epyon Translations'                                                   : pfuncs_a_g.extractEpyonTranslations,
				'Ero Light Novel Translations'                                         : pfuncs_a_g.extractEroLightNovelTranslations,
				'Eros Workshop'                                                        : pfuncs_a_g.extractErosWorkshop,
				'Eternal Dreamland Translation'                                        : pfuncs_a_g.extractEternalDreamlandTranslation,
				'eternalpath.net'                                                      : pfuncs_a_g.extractEternalpath,
				'Etheria Translations'                                                 : pfuncs_a_g.extractEtheriaTranslations,
				'Eugene Rain'                                                          : pfuncs_a_g.extractEugeneRain,
				'Eugene Woodbury'                                                      : pfuncs_a_g.extractEugeneWoodbury,
				'Evening Boat Translations'                                            : pfuncs_a_g.extractEveningBoatTranslations,
				'Ever Night Blog'                                                      : pfuncs_a_g.extractEverNightBlog,
				'ExMachina.Asia'                                                       : pfuncs_a_g.extractExMachinaAsia,
				'Explore'                                                              : pfuncs_a_g.extractExplore,
				'ExpNull'                                                              : pfuncs_a_g.extractExpNull,
				'Extant Visions'                                                       : pfuncs_a_g.extractExtantVisions,
				'Eye of Adventure '                                                    : pfuncs_a_g.extractEyeofAdventure,
				'EZ Translations'                                                      : pfuncs_a_g.extractEZTranslations,
				'Fable Wind'                                                           : pfuncs_a_g.extractFableWind,
				'FailTranslations'                                                     : pfuncs_a_g.extractFailTranslations,
				'Fairly Accurate Translations'                                         : pfuncs_a_g.extractFairlyAccurateTranslations,
				'Fak Translations'                                                     : pfuncs_a_g.extractFakTranslations,
				'Fake Fruit Translation'                                               : pfuncs_a_g.extractFakeFruitTranslation,
				'Fake Fruits Translations'                                             : pfuncs_a_g.extractFakeFruitsTranslations,
				'Fake typist'                                                          : pfuncs_a_g.extractFaketypist,
				'Fake USAW Translation'                                                : pfuncs_a_g.extractFakeUsawTranslation,
				'Falamar Translation'                                                  : pfuncs_a_g.extractFalamarTranslation,
				'Falinmer'                                                             : pfuncs_a_g.extractFalinmer,
				'Fanatical'                                                            : pfuncs_a_g.extractFanatical,
				'Fantasy Novels'                                                       : pfuncs_a_g.extractFantasyNovels,
				'Fantasy novels'                                                       : pfuncs_a_g.extractFantasyNovels,
				'Fantasy-Books'                                                        : pfuncs_a_g.extractFantasyBooksLive,
				'fantasy-books.live'                                                   : pfuncs_a_g.extractFantasyBooksLive,
				'Fate and Affinity'                                                    : pfuncs_a_g.extractFateAndAffinity,
				'FeedProxy'                                                            : pfuncs_a_g.extractFeedProxy,
				'Feels Bad Translation'                                                : pfuncs_a_g.extractFeelsBadTranslation,
				'Feels Bad Translations'                                               : pfuncs_a_g.extractFeelsBadTranslations,
				'FF'                                                                   : pfuncs_a_g.extractFf,
				'fgiLaN translations'                                                  : pfuncs_a_g.extractfgiLaNTranslations,
				'Fighting Dreamers Scanlations'                                        : pfuncs_a_g.extractFightingDreamersScanlations,
				'Firebird\'s Nest'                                                     : pfuncs_a_g.extractFirebirdsNest,
				'Five Star Specialists'                                                : pfuncs_a_g.extractFiveStar,
				'Fleeting Phoenix Translations'                                        : pfuncs_a_g.extractFleetingPhoenixTranslations,
				'Flicker Hero'                                                         : pfuncs_a_g.extractFlickerHero,
				'Flower Bridge Too'                                                    : pfuncs_a_g.extractFlowerBridgeToo,
				'For Kalimdor!'                                                        : pfuncs_a_g.extractForKalimdor,
				'Forbidentry'                                                          : pfuncs_a_g.extractForbidentry,
				'Forgetful Dreamer'                                                    : pfuncs_a_g.extractForgetfulDreamer,
				'Forgotten Conqueror'                                                  : pfuncs_a_g.extractForgottenConqueror,
				'Forthemoney Translations'                                             : pfuncs_a_g.extractForthemoneyTranslations,
				'FraiziarTL'                                                           : pfuncs_a_g.extractFraiziartl,
				'Freezing Light Novels'                                                : pfuncs_a_g.extractFreezingLightNovels,
				'Friendship Is Power'                                                  : pfuncs_a_g.extractFriendshipIsPower,
				'Frostfire 10'                                                         : pfuncs_a_g.extractFrostfire10,
				'Frozen\'s Lazy Blog'                                                  : pfuncs_a_g.extractFrozensLazyBlog,
				'Fudge Translations'                                                   : pfuncs_a_g.extractFudgeTranslations,
				'Fung Shen'                                                            : pfuncs_a_g.extractFungShen,
				'FunWithStela'                                                         : pfuncs_a_g.extractFunwithstela,
				'Fuwa Fuwa Tales~'                                                     : pfuncs_a_g.extractFuwaFuwaTales,
				'Fuzion Life'                                                          : pfuncs_a_g.extractFuzionLife,
				'Game of Scanlation'                                                   : pfuncs_a_g.extractGameOfScanlation,
				'Gaochao Translations'                                                 : pfuncs_a_g.extractGaochaoTranslations,
				'Gargoyle Web Serial'                                                  : pfuncs_a_g.extractGargoyleWebSerial,
				'Gila Translation Monster'                                             : pfuncs_a_g.extractGilaTranslation,
				'Giraffe Corps'                                                        : pfuncs_a_g.extractGiraffe,
				'Girly Novels'                                                         : pfuncs_a_g.extractGirlyNovels,
				'God Awful Machine Translator'                                         : pfuncs_a_g.extractGodAwfulMachineTranslator,
				'Goddess! Grant Me a Girlfriend!!'                                     : pfuncs_a_g.extractGoddessGrantMeaGirlfriend,
				'Gomigeemu'                                                            : pfuncs_a_g.extractGomigeemu,
				'Good Wife Translation'                                                : pfuncs_a_g.extractGoodWifeTranslation,
				'Grandlation'                                                          : pfuncs_a_g.extractGrandlation,
				'Gravity Tales'                                                        : pfuncs_a_g.extractGravityTranslation,
				'Gravity Translation'                                                  : pfuncs_a_g.extractGravityTranslation,
				'GrimdarkZ Translations'                                               : pfuncs_a_g.extractGrimdarkZTranslations,
				'Grow with Me'                                                         : pfuncs_a_g.extractGrowWithMe,
				'Grow with me'                                                         : pfuncs_a_g.extractGrowWithMe,
				'guhehe.TRANSLATIONS'                                                  : pfuncs_a_g.extractGuhehe,
				'Gundam Wing Tales'                                                    : pfuncs_a_g.extractGundamWingTales,
				'Guro Translation'                                                     : pfuncs_a_g.extractGuroTranslation,
				'Guro\'s Library of Stories'                                           : pfuncs_a_g.extractGurosLibraryofStories,
				'Hachidori Translations'                                               : pfuncs_h_n.extractHachidoriTranslations,
				'Hajiko translation'                                                   : pfuncs_h_n.extractHajiko,
				'Hakureina'                                                            : pfuncs_h_n.extractHakureina,
				'Hakushaku to Yousei'                                                  : pfuncs_h_n.extractHakushakuToYousei,
				'Halcyon Translations'                                                 : pfuncs_h_n.extractHalcyonTranslations,
				'HalfElementMaster Translation'                                        : pfuncs_h_n.extractHalfElementMasterTranslation,
				'Hamster428'                                                           : pfuncs_h_n.extractHamster428,
				'Hanashi Oba-san'                                                      : pfuncs_h_n.extractHanashiObasan,
				'Happythexceed の Corner'                                               : pfuncs_h_n.extractHappythexceedのCorner,
				'Haru no Sutori'                                                       : pfuncs_h_n.extractHaruNoSutori,
				'HaruChika & Ghost Hunt Translations'                                  : pfuncs_h_n.extractHaruchikaGhostHuntTranslations,
				'HaruPARTY'                                                            : pfuncs_h_n.extractHaruPARTY,
				'Haru★'                                                                : pfuncs_h_n.extractHaru,
				'Hasutsuki'                                                            : pfuncs_h_n.extractHasutsuki,
				'Heart Crusade Scans'                                                  : pfuncs_h_n.extractHeartCrusadeScans,
				'Heavenly Star Translations'                                           : pfuncs_h_n.extractHeavenlyStarTranslations,
				'Heavens Justice Translation'                                          : pfuncs_h_n.extractHeavensJusticeTranslation,
				'Helidwarf'                                                            : pfuncs_h_n.extractHelidwarf,
				'Hell Yeah 524'                                                        : pfuncs_h_n.extractHellYeah524,
				'Hello Translations'                                                   : pfuncs_h_n.extractHelloTranslations,
				'Hellping'                                                             : pfuncs_h_n.extractHellping,
				'Hellsing Federation Translations'                                     : pfuncs_h_n.extractHellsingFederationTranslations,
				'Hendricksen-sama'                                                     : pfuncs_h_n.extractHendricksensama,
				'Henouji Translation'                                                  : pfuncs_h_n.extractHenoujiTranslation,
				'Heroic Legend of Arslan Translations'                                 : pfuncs_h_n.extractHeroicLegendOfArslanTranslations,
				'Heroic Novels'                                                        : pfuncs_h_n.extractHeroicNovels,
				'Hikki no Mori Translations'                                           : pfuncs_h_n.extractHikkinoMoriTranslations,
				'Himegami no Miko Translated'                                          : pfuncs_h_n.extractHimegamiNoMikoTranslated,
				'Hiohbye Translations'                                                 : pfuncs_h_n.extractHiohbyeTranslations,
				'Hokage Translations'                                                  : pfuncs_h_n.extractHokageTrans,
				'Hold \'X\' and Click'                                                 : pfuncs_h_n.extractHoldX,
				'Hot Cocoa Translations'                                               : pfuncs_h_n.extractHotCocoa,
				'Hyorinmaru Blog'                                                      : pfuncs_h_n.extractHyorinmaruBlog,
				'Hyorinmaru'                                                           : pfuncs_h_n.extractHyorinmaruBlog,
				'I Ballistic Bunnies'                                                  : pfuncs_h_n.extractIBallisticBunnies,
				'I only want Shinji.'                                                  : pfuncs_h_n.extractIOnlyWantShinji,
				'I Speak MTL'                                                          : pfuncs_h_n.extractISpeakMtl,
				'I swear I\'m not lost... I\'m just... exploring...'                   : pfuncs_h_n.extractISwearIMNotLostIMJustExploring,
				'I\'ve reincarnated, but I\'m a Girl! Wait, am I not even Human?'      : pfuncs_h_n.extractIVeReincarnatedButIMAGirlWaitAmINotEvenHuman,
				'IAmABanana Freshie Translation V2'                                    : pfuncs_h_n.extractIamabananaFreshieTranslationV2,
				'IAmABanana Freshie Translation'                                       : pfuncs_h_n.extractIAmABananaFreshieTranslation,
				'Icarus Bride Scanlation'                                              : pfuncs_h_n.extractIcarusBrideScanlation,
				'Icarus'                                                               : pfuncs_h_n.extractIcarus,
				'Ichinichi BL'                                                         : pfuncs_h_n.extractIchinichiBl,
				'Idyllic Translations'                                                 : pfuncs_h_n.extractIdyllicTranslations,
				'Imoutolicious Light Novel Translations'                               : pfuncs_h_n.extractImoutolicious,
				'Imperator'                                                            : pfuncs_h_n.extractImperator,
				'In My Daydreams'                                                      : pfuncs_h_n.extractInMyDaydreams,
				'Inaccurate Translations'                                              : pfuncs_h_n.extractInaccurateTranslations,
				'Incarneous'                                                           : pfuncs_h_n.extractIncarneous,
				'Incarose Jealousy MTL'                                                : pfuncs_h_n.extractIncaroseJealousyMTL,
				'Inchoate Oeuvre'                                                      : pfuncs_h_n.extractInchoateOeuvre,
				'Indonesian Story Translatio'                                          : pfuncs_h_n.extractIndonesianStoryTranslatio,
				'Infinite Novel Translations'                                          : pfuncs_h_n.extractInfiniteNovelTranslations,
				'Infinite Translations'                                                : pfuncs_h_n.extractInfiniteTranslations,
				'Infinity Translations'                                                : pfuncs_h_n.extractInfinityTranslations,
				'Insane Translations'                                                  : pfuncs_h_n.extractInsaneTranslations,
				'Insignia Pierce'                                                      : pfuncs_h_n.extractKnW,
				'IntenseDesSugar'                                                      : pfuncs_h_n.extractIntenseDesSugar,
				'Isekai Fiction'                                                       : pfuncs_h_n.extractIsekaiFiction,
				'Isekai Mahou Translations!'                                           : pfuncs_h_n.extractIsekaiMahou,
				'Isekai Soul-Cyborg Translations'                                      : pfuncs_h_n.extractIsekaiTranslation,
				'Isolarium'                                                            : pfuncs_h_n.extractIsolarium,
				'Istian\'s Workshop'                                                   : pfuncs_h_n.extractIstiansWorkshop,
				'Iterations within a Thought-Eclipse'                                  : pfuncs_h_n.extractIterations,
				'itranslateln'                                                         : pfuncs_h_n.extractItranslateln,
				'izra709 | B Group no Shounen Translations'                            : pfuncs_h_n.extractIzra709,
				'Jagaimo'                                                              : pfuncs_h_n.extractJagaimo,
				'Januke Translations'                                                  : pfuncs_h_n.extractJanukeTranslations,
				'Japanese Light Novels: Prologues'                                     : pfuncs_h_n.extractJapaneseLightNovelsPrologues,
				'Japanese Novel Translation'                                           : pfuncs_h_n.extractJapaneseNovelTranslation,
				'Japanese Novel'                                                       : pfuncs_h_n.extractJapaneseNovel,
				'Japtem'                                                               : pfuncs_h_n.extractJaptem,
				'Jawz Publications'                                                    : pfuncs_h_n.extractJawzPublications,
				'JawzTranslations'                                                     : pfuncs_h_n.extractJawzTranslations,
				'Jen Press Translation'                                                : pfuncs_h_n.extractJenPressTranslation,
				'JeruTz\'s Blog'                                                       : pfuncs_h_n.extractJeruTzsBlog,
				'Joeglen\'s Translation Space'                                         : pfuncs_h_n.extractJoeglensTranslationSpace,
				'Joeglens\' Translation Space'                                         : pfuncs_h_n.extractJoeglensTranslationSpace,
				'Joie de Vivre'                                                        : pfuncs_h_n.extractJoiedeVivre,
				'JoleCole\'s Station'                                                  : pfuncs_h_n.extractJolecoleSStation,
				'JuJu Translation'                                                     : pfuncs_h_n.extractJuJuTranslation,
				'Jun Juntianxia'                                                       : pfuncs_h_n.extractJunJuntianxia,
				'Junk Burst Translations'                                              : pfuncs_h_n.extractJunkBurstTranslations,
				'Just BL Things'                                                       : pfuncs_h_n.extractJustBlThings,
				'Jynki\'s TLs'                                                         : pfuncs_h_n.extractJynkisTLs,
				'Kaezar Translations'                                                  : pfuncs_h_n.extractKaezar,
				'Kaguro Jp'                                                            : pfuncs_h_n.extractKaguroJp,
				'Kahoim Translations'                                                  : pfuncs_h_n.extractKahoim,
				'Kai\'s Translations'                                                  : pfuncs_h_n.extractKaisTranslations,
				'Kakaoo Story'                                                         : pfuncs_h_n.extractKakaooStory,
				'Kakkokari (仮)'                                                        : pfuncs_h_n.extractKakkokari仮,
				'Kakkokari'                                                            : pfuncs_h_n.extractKakkokari,
				'Kami Translation'                                                     : pfuncs_h_n.extractKamiTranslation,
				'Kawaii Daikon'                                                        : pfuncs_h_n.extractKawaiiDaikon,
				'Kazama Translation'                                                   : pfuncs_h_n.extractKazamaTranslation,
				'Kedelu'                                                               : pfuncs_h_n.extractKedelu,
				'Kencephalon Translations'                                             : pfuncs_h_n.extractKencephalonTranslations,
				'Kenkyo Reika'                                                         : pfuncs_h_n.extractKenkyoReika,
				'Kerambit\'s Incisions'                                                : pfuncs_h_n.extractKerambit,
				'Keyo Translations'                                                    : pfuncs_h_n.extractKeyoTranslations,
				'Kidney Translations'                                                  : pfuncs_h_n.extractKidneyTranslations,
				'King Jaahn\'s Subjects'                                               : pfuncs_h_n.extractKingJaahn,
				'Kiri Leaves'                                                          : pfuncs_h_n.extractKiri,
				'Kirihara Maya'                                                        : pfuncs_h_n.extractKiriharaMaya,
				'Kiriko Translations'                                                  : pfuncs_h_n.extractKirikoTranslations,
				'Kisato\'s Hobbies!'                                                   : pfuncs_h_n.extractKisatoSHobbies,
				'Kisato\'s MLTs'                                                       : pfuncs_h_n.extractKisatosMLTs,
				'KitaKami Ooi'                                                         : pfuncs_h_n.extractKitaKamiOoi,
				'Kiyoitsukikage'                                                       : pfuncs_h_n.extractKiyoitsukikage,
				'KN Translation'                                                       : pfuncs_h_n.extractKNTranslation,
				'Knight Fantastic Night Translations'                                  : pfuncs_h_n.extractKnightFantasticNightTranslations,
				'Knokkro Translations'                                                 : pfuncs_h_n.extractKnokkroTranslations,
				'KobatoChanDaiSukiScan'                                                : pfuncs_h_n.extractKobatoChanDaiSukiScan,
				'Kokuma Translations'                                                  : pfuncs_h_n.extractKokumaTranslations,
				'KONDEE Translations'                                                  : pfuncs_h_n.extractKONDEETranslations,
				'Konjiki no Wordmaster'                                                : pfuncs_h_n.extractKnW,
				'Konko\'s Translations'                                                : pfuncs_h_n.extractKonkoSTranslations,
				'Konobuta'                                                             : pfuncs_h_n.extractKonobuta,
				'Koong Koong Translations'                                             : pfuncs_h_n.extractKoongKoongTranslations,
				'Kore Yori Hachidori'                                                  : pfuncs_h_n.extractKoreYoriHachidori,
				'Korean Novel Translations'                                            : pfuncs_h_n.extractKoreanNovelTrans,
				'Krytyk\'s Translations'                                               : pfuncs_h_n.extractKrytyksTranslations,
				'Kuda Lakorn'                                                          : pfuncs_h_n.extractKudaLakorn,
				'Kudarajin'                                                            : pfuncs_h_n.extractKudarajin,
				'Kuma Otou'                                                            : pfuncs_h_n.extractKumaOtou,
				'Kuro Translation'                                                     : pfuncs_h_n.extractKuroTranslation,
				'Kuro Translations'                                                    : pfuncs_h_n.extractKuroTranslations,
				'Kuromin'                                                              : pfuncs_h_n.extractKuromin,
				'Kuros TL'                                                             : pfuncs_h_n.extractKurosTL,
				'Kurotsuki Novel'                                                      : pfuncs_h_n.extractKurotsukiNovel,
				'Kuso Machine Translation'                                             : pfuncs_h_n.extractKusoMachineTranslation,
				'Kyakka Translations'                                                  : pfuncs_h_n.extractKyakkaTranslations,
				'Kyakka'                                                               : pfuncs_h_n.extractKyakka,
				'KyOption\'s Library'                                                  : pfuncs_h_n.extractKyOptionsLibrary,
				'kyoptionslibrary.blogspot.com'                                        : pfuncs_h_n.extractKyOptionsLibrary,
				'L2M'                                                                  : pfuncs_h_n.extractL2M,
				'L3D'                                                                  : pfuncs_h_n.extractL3D,
				'Laki\'s Laboratory'                                                   : pfuncs_h_n.extractLakisLaboratory,
				'Land of Light Novels'                                                 : pfuncs_h_n.extractLandofLightNovels,
				'LannyLand'                                                            : pfuncs_h_n.extractLannyland,
				'Larvyde'                                                              : pfuncs_h_n.extractLarvyde,
				'Lascivious Imouto'                                                    : pfuncs_h_n.extractLasciviousImouto,
				'Lastvoice Translator'                                                 : pfuncs_h_n.extractLastvoiceTranslator,
				'Laughing Ghoul Translations'                                          : pfuncs_h_n.extractLaughingGhoulTranslations,
				'Laute, Laute!'                                                        : pfuncs_h_n.extractLauteLaute,
				'Layzisheep'                                                           : pfuncs_h_n.extractLayzisheep,
				'Lazy G Translations'                                                  : pfuncs_h_n.extractLazyGTranslations,
				'Lazy Nanaseru Translation'                                            : pfuncs_h_n.extractLazyNanaseruTranslation,
				'Lazy NEET Translations'                                               : pfuncs_h_n.extractNEET,
				'Leecher Vamparis Translations'                                        : pfuncs_h_n.extractLeecherVamparisTranslations,
				'Legend of Galactic Heroes Translation Project'                        : pfuncs_h_n.extractLegendofGalacticHeroes,
				'Legend of the Evil God'                                               : pfuncs_h_n.extractLegendoftheEvilGod,
				'Legions Realm'                                                        : pfuncs_h_n.extractLegionsRealm,
				'LESYT'                                                                : pfuncs_h_n.extractLESYT,
				'Levity Tales'                                                         : pfuncs_h_n.extractLevityTales,
				'levitytales.com'                                                      : pfuncs_h_n.extractLevityTales,
				'Lickymee Translations'                                                : pfuncs_h_n.extractLickymeeTranslations,
				'Light Novel Bastion'                                                  : pfuncs_h_n.extractLightNovelBastion,
				'Light Novel Cafe'                                                     : pfuncs_h_n.extractLightNovelCafe,
				'Light Novel translations'                                             : pfuncs_h_n.extractLightNoveltranslations,
				'Light Novels Translations !'                                          : pfuncs_h_n.extractLightNovelsTranslations,
				'Light Novels Translations'                                            : pfuncs_h_n.extractLightNovelsTranslations,
				'Light Novels with Misa-chan~'                                         : pfuncs_h_n.extractLightNovelswithMisachan,
				'Light Novels World'                                                   : pfuncs_h_n.extractLightNovelsWorld,
				'Light Novels'                                                         : pfuncs_h_n.extractLightNovels,
				'Lil\' Bliss Novels'                                                   : pfuncs_h_n.extractLilBlissNovels,
				'Lily Ros 3'                                                           : pfuncs_h_n.extractLilyRos3,
				'Ling Translates Sometimes'                                            : pfuncs_h_n.extractLingTranslatesSometimes,
				'Lingson\'s Translations'                                              : pfuncs_h_n.extractLingson,
				'Linked Translations'                                                  : pfuncs_h_n.extractLinkedTranslations,
				'Lion Mask\'s Really Professional Translations'                        : pfuncs_h_n.extractLionMasksReallyProfessionalTranslations,
				'Little Novel Translation'                                             : pfuncs_h_n.extractLittleNovelTranslation,
				'Little Translations'                                                  : pfuncs_h_n.extractLittleTranslations,
				'LittleShanks Translations'                                            : pfuncs_h_n.extractLittleShanksTranslations,
				'Lizard Translations'                                                  : pfuncs_h_n.extractLizardTranslations,
				'Llian'                                                                : pfuncs_h_n.extractLlian,
				'LMS Machine Translations'                                             : pfuncs_h_n.extractLMSMachineTranslations,
				'Ln Addiction'                                                         : pfuncs_h_n.extractLnAddiction,
				'LNTranslation'                                                        : pfuncs_h_n.extractLntranslation,
				'Loathsome Translations'                                               : pfuncs_h_n.extractLoathsomeTranslations,
				'Logatse Translations'                                                 : pfuncs_h_n.extractLogatseTranslations,
				'Lohithbb TLs'                                                         : pfuncs_h_n.extractLohithbbTLs,
				'Loiterous'                                                            : pfuncs_h_n.extractLoiterous,
				'Loli Translations'                                                    : pfuncs_h_n.extractLoliTranslations,
				'Loliquent'                                                            : pfuncs_h_n.extractKnW,
				'Lonahora'                                                             : pfuncs_h_n.extractLonahora,
				'LorCromwell'                                                          : pfuncs_h_n.extractLorCromwell,
				'LordofScrubs'                                                         : pfuncs_h_n.extractLordofScrubs,
				'Lost in Translation'                                                  : pfuncs_h_n.extractLostInTranslation,
				'Love me if you dare'                                                  : pfuncs_h_n.extractLoveMeIfYouDare,
				'Lovely x Day'                                                         : pfuncs_h_n.extractLovelyxDay,
				'Lt.Beefy\'s MTL'                                                      : pfuncs_h_n.extractLtBeefySMtl,
				'Luen Translations'                                                    : pfuncs_h_n.extractLuenTranslations,
				'Luminaeris'                                                           : pfuncs_h_n.extractLuminaeris,
				'Luminstia'                                                            : pfuncs_h_n.extractLuminstia,
				'Lunaris'                                                              : pfuncs_h_n.extractLunaris,
				'Lunate'                                                               : pfuncs_h_n.extractLunate,
				'Luxiufer'                                                             : pfuncs_h_n.extractLuxiufer,
				'LygarTranslations'                                                    : pfuncs_h_n.extractLygarTranslations,
				'Lylis Translations'                                                   : pfuncs_h_n.extractLylisTranslations,
				'Lynfamily'                                                            : pfuncs_h_n.extractLynfamily,
				'Lypheon Machine Translation'                                          : pfuncs_h_n.extractLypheonMachineTranslation,
				'Machine Sliced Bread'                                                 : pfuncs_h_n.extractMachineSlicedBread,
				'Madao Translations'                                                   : pfuncs_h_n.extractMadaoTranslations,
				'MadoSpicy TL'                                                         : pfuncs_h_n.extractMadoSpicy,
				'Mage Life'                                                            : pfuncs_h_n.extractMageLife,
				'Magictrans'                                                           : pfuncs_h_n.extractMagictrans,
				'Mahou Koukoku'                                                        : pfuncs_h_n.extractMahouKoukoku,
				'Mahoutsuki Translation'                                               : pfuncs_h_n.extractMahoutsuki,
				'Maki Translates'                                                      : pfuncs_h_n.extractMakiTranslates,
				'Makina Translations'                                                  : pfuncs_h_n.extractMakinaTranslations,
				'Mana Tank Magus'                                                      : pfuncs_h_n.extractManaTankMagus,
				'Manga0205 Translations'                                               : pfuncs_h_n.extractManga0205Translations,
				'Manlyflower Translations'                                             : pfuncs_h_n.extractManlyflowerTranslations,
				'Maou na Anoko to murabito a'                                          : pfuncs_h_n.extractMaounaAnokotomurabitoa,
				'Martial Dao'                                                          : pfuncs_h_n.extractMartialDao,
				'Martial God Translator'                                               : pfuncs_h_n.extractMartialGodTranslator,
				'Mecha Mushroom Translations'                                          : pfuncs_h_n.extractMechaMushroom,
				'Medium Well Translations'                                             : pfuncs_h_n.extractMediumWellTranslations,
				'Meteor Ranger T.'                                                     : pfuncs_h_n.extractMeteorRangerT,
				'Meteoremperor-san'                                                    : pfuncs_h_n.extractMeteoremperorSan,
				'MGRP Translations'                                                    : pfuncs_h_n.extractMgrpTranslations,
				'Midnight Translation Blog'                                            : pfuncs_h_n.extractMidnightTranslationBlog,
				'Mikagura Scanlations Club'                                            : pfuncs_h_n.extractMikaguraScanlationsClub,
				'Mike777ac'                                                            : pfuncs_h_n.extractMike777ac,
				'Mineral Water Translation'                                            : pfuncs_h_n.extractMineralWaterTranslation,
				'Misty Cloud Translations'                                             : pfuncs_h_n.extractMistyCloudTranslations,
				'Mittens 220'                                                          : pfuncs_h_n.extractMittens220,
				'Miumiu\'s musings'                                                    : pfuncs_h_n.extractMiumiuSMusings,
				'Mnemeaa'                                                              : pfuncs_h_n.extractMnemeaa,
				'Mobile Suit Zeta Gundam Novels Translation'                           : pfuncs_h_n.extractMobileSuitZetaGundamNovelsTranslation,
				'Mofumofu Translation'                                                 : pfuncs_h_n.extractMofumofuTranslation,
				'Mojo Translations'                                                    : pfuncs_h_n.extractMojoTranslations,
				'Monk Translation'                                                     : pfuncs_h_n.extractMonkTranslation,
				'Moon Bunny Cafe'                                                      : pfuncs_h_n.extractMoonBunnyCafe,
				'Moon Rabbit Translations'                                             : pfuncs_h_n.extractMoonRabbitTranslations,
				'Moonlight Translations'                                               : pfuncs_h_n.extractMoonlightTranslations,
				'Morrighan Sucks'                                                      : pfuncs_h_n.extractMorrighanSucks,
				'Mountain of Pigeons Translations'                                     : pfuncs_h_n.extractMountainofPigeonsTranslations,
				'Mousou Haven'                                                         : pfuncs_h_n.extractMousouHaven,
				'mousou-haven.com'                                                     : pfuncs_h_n.extractMousouhaven,
				'MT Novels'                                                            : pfuncs_h_n.extractMTNovels,
				'MTLCrap'                                                              : pfuncs_h_n.extractMTLCrap,
				'My First Time Translating'                                            : pfuncs_h_n.extractMyFirstTimeTranslating,
				'My Purple World'                                                      : pfuncs_h_n.extractMyPurpleWorld,
				'My Translations'                                                      : pfuncs_h_n.extractMyTranslations,
				'MyEngTranslation'                                                     : pfuncs_h_n.extractMyEngTranslation,
				'Myoniyoni Translations'                                               : pfuncs_h_n.extractMyoniyoniTranslations,
				'Mystic Tales'                                                         : pfuncs_h_n.extractMysticTales,
				'Mystique Translations'                                                : pfuncs_h_n.extractMystiqueTranslations,
				'Mythical Pagoda'                                                      : pfuncs_h_n.extractMythicalPagoda,
				'N00b Translations'                                                    : pfuncs_h_n.extractN00bTranslations,
				'Nadenadeshitai'                                                       : pfuncs_h_n.extractNadenadeshitai,
				'Nakimushi'                                                            : pfuncs_h_n.extractNakimushi,
				'Nanjamora'                                                            : pfuncs_h_n.extractNanjamora,
				'NanoDesu Light Novel Translations'                                    : pfuncs_h_n.extractNanoDesuLightNovelTranslations,
				'Nanodesu'                                                             : pfuncs_h_n.extractNanodesu,
				'Nanowave Translations'                                                : pfuncs_h_n.extractNanowaveTranslations,
				'National NEET'                                                        : pfuncs_h_n.extractNationalNEET,
				'Natsu TL'                                                             : pfuncs_h_n.extractNatsuTl,
				'NEET Translations'                                                    : pfuncs_h_n.extractNeetTranslations,
				'Nega Translations'                                                    : pfuncs_h_n.extractNegaTranslations,
				'Negative Inserts'                                                     : pfuncs_h_n.extractNegativeInserts,
				'Nekoyashiki'                                                          : pfuncs_h_n.extractNekoyashiki,
				'Neo DIR'                                                              : pfuncs_h_n.extractNeoDir,
				'Neo Translations'                                                     : pfuncs_h_n.extractNeoTranslations,
				'Nepustation'                                                          : pfuncs_h_n.extractNepustation,
				'Nex Serus'                                                            : pfuncs_h_n.extractNexSerus,
				'Next level for the PLOT'                                              : pfuncs_h_n.extractNextlevelforthePLOT,
				'Nieracol Translations'                                                : pfuncs_h_n.extractNieracolTranslations,
				'Nightbreeze Translations'                                             : pfuncs_h_n.extractNightbreeze,
				'NightFall Translations'                                               : pfuncs_h_n.extractNightFallTranslations,
				'Niiselin'                                                             : pfuncs_h_n.extractNiiselin,
				'NinjaNUF'                                                             : pfuncs_h_n.extractNinjaNUF,
				'Ninth Charmolypi Translation'                                         : pfuncs_h_n.extractNinthCharmolypiTranslation,
				'No Name Translations'                                                 : pfuncs_h_n.extractNoNameTranslations,
				'Nohohon Translation'                                                  : pfuncs_h_n.extractNohohon,
				'Noob Mtl'                                                             : pfuncs_h_n.extractNoobMtl,
				'Nooblate'                                                             : pfuncs_h_n.extractNooblate,
				'Noodletown Translated'                                                : pfuncs_h_n.extractNoodletownTranslated,
				'Norva Blog'                                                           : pfuncs_h_n.extractNorvaBlog,
				'Nostalgia on 9th Avenue'                                              : pfuncs_h_n.extractNostalgiaOn9ThAvenue,
				'NOT Daily Translations'                                               : pfuncs_h_n.extractNotDailyTranslations,
				'Novel 361'                                                            : pfuncs_h_n.extractNovel361,
				'Novel Affairs'                                                        : pfuncs_h_n.extractNovelAffairs,
				'Novel Saga'                                                           : pfuncs_h_n.extractNovelSaga,
				'Novel Sanctuary'                                                      : pfuncs_h_n.extractNovelSanctuary,
				'Novel Square'                                                         : pfuncs_h_n.extractNovelSquare,
				'Novel Trans'                                                          : pfuncs_h_n.extractNovelTrans,
				'NovelCow'                                                             : pfuncs_h_n.extractNovelCow,
				'Novelisation'                                                         : pfuncs_h_n.extractNovelisation,
				'Novella Translation'                                                  : pfuncs_h_n.extractNovellaTranslation,
				'Novels Ground'                                                        : pfuncs_h_n.extractNovelsGround,
				'Novels Japan'                                                         : pfuncs_h_n.extractNovelsJapan,
				'Novels Nao'                                                           : pfuncs_h_n.extractNovelsNao,
				'Novels Reborn'                                                        : pfuncs_h_n.extractNovelsReborn,
				'Novels Translation'                                                   : pfuncs_h_n.extractNovelsTranslation,
				'Novels Travel'                                                        : pfuncs_h_n.extractNovelsTravel,
				'Novels&Chill'                                                         : pfuncs_h_n.extractNovelsChill,
				'NoviceTranslator'                                                     : pfuncs_h_n.extractNoviceTranslator,
				'Novitranslation'                                                      : pfuncs_h_n.extractNovitranslation,
				'Nowhere & Nothing'                                                    : pfuncs_h_n.extractNowhereNothing,
				'NTRHolic'                                                             : pfuncs_h_n.extractNTRHolic,
				'Nusantara Cafe'                                                       : pfuncs_h_n.extractNusantaraCafe,
				'Nutty is Procrastinating'                                             : pfuncs_h_n.extractNutty,
				'O6asan\'s Web Site'                                                   : pfuncs_o_u.extractO6AsanSWebSite,
				'Obsessive Dreamer'                                                    : pfuncs_o_u.extractObsessiveDreamer,
				'Odd Squad Novels'                                                     : pfuncs_o_u.extractOddSquadNovels,
				'Ohanashimi'                                                           : pfuncs_o_u.extractOhanashimi,
				'OK Translation'                                                       : pfuncs_o_u.extractOKTranslation,
				'Omega Harem'                                                          : pfuncs_o_u.extractOmegaHarem,
				'Omgitsaray Translations'                                              : pfuncs_o_u.extractOmgitsaray,
				'omgitsaray translations'                                              : pfuncs_o_u.extractOmgitsarayTranslations,
				'One Man Army Translations (OMA)'                                      : pfuncs_o_u.extractOneManArmy,
				'One Man Army Translations'                                            : pfuncs_o_u.extractOneManArmy,
				'One Second Spring'                                                    : pfuncs_o_u.extractOneSecondSpring,
				'OOO Translations'                                                     : pfuncs_o_u.extractOOOTranslations,
				'Open The Sky'                                                         : pfuncs_o_u.extractOpenTheSky,
				'Opinisaya.com'                                                        : pfuncs_o_u.extractOpinisaya,
				'OppaTranslations'                                                     : pfuncs_o_u.extractOppaTranslations,
				'Orange Translations'                                                  : pfuncs_o_u.extractOrangeTranslations,
				'Ore ga Heroine in English'                                            : pfuncs_o_u.extractOregaHeroineinEnglish,
				'Origin Novels'                                                        : pfuncs_o_u.extractOriginNovels,
				'Orinjido Scans'                                                       : pfuncs_o_u.extractOrinjidoScans,
				'Otome Revolution'                                                     : pfuncs_o_u.extractOtomeRevolution,
				'Otsumi'                                                               : pfuncs_o_u.extractOtsumi,
				'Otterspace Translation'                                               : pfuncs_o_u.extractOtterspaceTranslation,
				'OtterSpace Translation'                                               : pfuncs_o_u.extractOtterspaceTranslation,
				'otterspacetranslation'                                                : pfuncs_o_u.extractOtterspaceTranslation,
				'Outspan Foster'                                                       : pfuncs_o_u.extractOutspanFoster,
				'Oyasumi Reads'                                                        : pfuncs_o_u.extractOyasumiReads,
				'Pact Web Serial'                                                      : pfuncs_o_u.extractPactWebSerial,
				'Paichun Translations'                                                 : pfuncs_o_u.extractPaichunTranslations,
				'Pajama Days'                                                          : pfuncs_o_u.extractPajamaDays,
				'Panda Translations'                                                   : pfuncs_o_u.extractPandaTranslations,
				'pandafuqtranslations'                                                 : pfuncs_o_u.extractPandafuqTranslations,
				'panisal'                                                              : pfuncs_o_u.extractPanisal,
				'Paradox Translations'                                                 : pfuncs_o_u.extractParadoxTranslations,
				'Paraphrase Translation'                                               : pfuncs_o_u.extractParaphraseTranslation,
				'Path of Translation'                                                  : pfuncs_o_u.extractPathOfTranslation,
				'Patriarch Reliance'                                                   : pfuncs_o_u.extractPatriarchReliance,
				'Paztok'                                                               : pfuncs_o_u.extractPaztok,
				'Pea Translation'                                                      : pfuncs_o_u.extractPeaTranslation,
				'Pea\'s Kingdom'                                                       : pfuncs_o_u.extractPeasKingdom,
				'Pegasus Farts'                                                        : pfuncs_o_u.extractPegasusFarts,
				'Pekabo Blog'                                                          : pfuncs_o_u.extractPekaboBlog,
				'Pengu Taichou'                                                        : pfuncs_o_u.extractPenguTaichou,
				'Penguin Overlord Translations'                                        : pfuncs_o_u.extractPenguinOverlordTranslations,
				'Penumbrale'                                                           : pfuncs_o_u.extractPenumbrale,
				'Pettanko Translations'                                                : pfuncs_o_u.extractPettankoTranslations,
				'PFC – Light Novel Translations'                                       : pfuncs_o_u.extractPFCLightNovelTranslations,
				'Pielord Translations'                                                 : pfuncs_o_u.extractPielordTranslations,
				'PiggyBottle Translations'                                             : pfuncs_o_u.extractPiggyBottleTranslations,
				'Pika Translations'                                                    : pfuncs_o_u.extractPikaTranslations,
				'Pippi Site'                                                           : pfuncs_o_u.extractPippiSite,
				'PlainlyBored'                                                         : pfuncs_o_u.extractPlainlyBored,
				'Plant Translation'                                                    : pfuncs_o_u.extractPlantTranslation,
				'Pleiades'                                                             : pfuncs_o_u.extractPleiades,
				'Polar Bear Catcher'                                                   : pfuncs_o_u.extractPolarBearCatcher,
				'Polaris Translations'                                                 : pfuncs_o_u.extractPolarisTranslations,
				'Polyphonic Story Translation Group'                                   : pfuncs_o_u.extractPolyphonicStoryTranslationGroup,
				'Poor Quality Translations'                                            : pfuncs_o_u.extractPoorQualityTranslations,
				'Popsiclete'                                                           : pfuncs_o_u.extractPopsiclete,
				'Popsiclete\'s'                                                        : pfuncs_o_u.extractPopsicleteS,
				'Premium Red Tea'                                                      : pfuncs_o_u.extractPremiumRedTea,
				'Priddles Translations'                                                : pfuncs_o_u.extractPriddlesTranslations,
				'Pride X ReVamp'                                                       : pfuncs_o_u.extractPrideXReVamp,
				'Prince of Stride Novel Translation'                                   : pfuncs_o_u.extractPrinceOfStrideNovelTranslation,
				'Prince Revolution!'                                                   : pfuncs_o_u.extractPrinceRevolution,
				'ProcrasTranslation'                                                   : pfuncs_o_u.extractProcrasTranslation,
				'Productive Procrastination'                                           : pfuncs_o_u.extractProductiveProcrastination,
				'ProfessionalGameThrower\'s Translations'                              : pfuncs_o_u.extractProfessionalGameThrowersTranslations,
				'Project Accelerator'                                                  : pfuncs_o_u.extractProjectAccelerator,
				'Proxy Translations'                                                   : pfuncs_o_u.extractProxyTranslations,
				'Psicern.Translations'                                                 : pfuncs_o_u.extractPsicernTranslations,
				'Psycho Barcode Translations'                                          : pfuncs_o_u.extractPsychoBarcodeTranslations,
				'Pumlated'                                                             : pfuncs_o_u.extractPumlated,
				'Pummels Translations'                                                 : pfuncs_h_n.extractKnW,
				'Pumpkin Translations'                                                 : pfuncs_o_u.extractPumpkinTranslations,
				'putttytranslations'                                                   : pfuncs_o_u.extractPuttty,
				'Qualidea of Scum and a Gold Coin'                                     : pfuncs_o_u.extractQualideaofScumandaGoldCoin,
				'QualiTeaTranslations'                                                 : pfuncs_o_u.extractQualiTeaTranslations,
				'Quality ★ Mistranslations'                                            : pfuncs_o_u.extractQualityMistranslations,
				'Radiant Translations'                                                 : pfuncs_o_u.extractRadiantTranslations,
				'Raenadel Translations'                                                : pfuncs_o_u.extractRaenadelTranslations,
				'Rainbow Translations'                                                 : pfuncs_o_u.extractRainbowTranslations,
				'Rainbow Turtle Translations'                                          : pfuncs_o_u.extractRainbowTurtleTranslations,
				'Rainy Translations'                                                   : pfuncs_o_u.extractRainyTranslations,
				'Raising Angels & Defection'                                           : pfuncs_o_u.extractRaisingAngelsDefection,
				'Raising the Dead'                                                     : pfuncs_o_u.extractRaisingTheDead,
				'RANCER'                                                               : pfuncs_o_u.extractRancer,
				'Rancer'                                                               : pfuncs_o_u.extractRancer,
				'Re:Library'                                                           : pfuncs_o_u.extractReLibrary,
				'Re:Monster Wiki'                                                      : pfuncs_o_u.extractReMonsterWiki,
				'Read Me Translations'                                                 : pfuncs_o_u.extractReadMeTranslations,
				'Reading Attic'                                                        : pfuncs_o_u.extractReadingAttic,
				'Realm of Chaos'                                                       : pfuncs_o_u.extractRealmOfChaos,
				'Rebirth Online World'                                                 : pfuncs_o_u.extractRebirthOnlineWorld,
				'Rebirth Online'                                                       : pfuncs_o_u.extractRebirthOnlineWorld,
				'Red Dragon Translations'                                              : pfuncs_o_u.extractRedDragonTranslations,
				'Red Lantern Archives'                                                 : pfuncs_o_u.extractRedLanternArchives,
				'Reddy Creations'                                                      : pfuncs_o_u.extractReddyCreations,
				'Refresh Translations'                                                 : pfuncs_o_u.extractRefreshTranslations,
				'Rei TransBlog'                                                        : pfuncs_o_u.extractReiTransBlog,
				'Reigokai: Isekai Translations'                                        : pfuncs_h_n.extractIsekaiTranslations,
				'Reincarnation Translations'                                           : pfuncs_o_u.extractReincarnationTranslations,
				'Reject Hero'                                                          : pfuncs_o_u.extractRejectHero,
				'Renegade Sanctuary'                                                   : pfuncs_o_u.extractRenegadeSanctuary,
				'Renna\'s Translations'                                                : pfuncs_o_u.extractRennaSTranslations,
				'Rhex\'s Translations'                                                 : pfuncs_o_u.extractRhexSTranslations,
				'Rhinabolla'                                                           : pfuncs_o_u.extractRhinabolla,
				'RidwanTrans'                                                          : pfuncs_o_u.extractRidwanTrans,
				'Ries Translations'                                                    : pfuncs_o_u.extractRiesTranslations,
				'Rinkage Translation'                                                  : pfuncs_o_u.extractRinkageTranslation,
				'RinOtakuBlog'                                                         : pfuncs_o_u.extractRinOtakuBlog,
				'Rinvelt House'                                                        : pfuncs_o_u.extractRinveltHouse,
				'Rip translations'                                                     : pfuncs_o_u.extractRiptranslations,
				'Rising Dragons Translation'                                           : pfuncs_o_u.extractRisingDragons,
				'Roasted Tea'                                                          : pfuncs_o_u.extractRoastedTea,
				'Rogue Apple'                                                          : pfuncs_o_u.extractRogueApple,
				'rokudenashi Translations'                                             : pfuncs_o_u.extractRokudenashiTranslations,
				'Romantic Dreamer\'s Sanctuary'                                        : pfuncs_o_u.extractRomanticDreamersSanctuary,
				'Root of Evil'                                                         : pfuncs_o_u.extractRootOfEvil,
				'Rosy Fantasy'                                                         : pfuncs_o_u.extractRosyFantasy,
				'Rosyfantasy - Always Dreaming'                                        : pfuncs_o_u.extractRosyFantasy,
				'Rotten Translations'                                                  : pfuncs_o_u.extractRottenTranslations,
				'Roxism HQ'                                                            : pfuncs_o_u.extractRoxism,
				'Royal Novel'                                                          : pfuncs_o_u.extractRoyalNovel,
				'Royal Road Weed'                                                      : pfuncs_o_u.extractRoyalRoadWeed,
				'Rozen Fantasy Translations'                                           : pfuncs_o_u.extractRozenFantasyTranslations,
				'RPG Novels'                                                           : pfuncs_o_u.extractRpgNovels,
				'RPGNovels'                                                            : pfuncs_o_u.extractRpgnovels,
				'Rumanshi\'s Lair'                                                     : pfuncs_o_u.extractRumanshisLair,
				'Rumor\'s Block'                                                       : pfuncs_o_u.extractRumorsBlock,
				'Ruze Translations'                                                    : pfuncs_o_u.extractRuzeTranslations,
				'S3ri'                                                                 : pfuncs_o_u.extractS3Ri,
				'Saber Translations'                                                   : pfuncs_o_u.extractSaberTranslations,
				'Sabishi desu!!'                                                       : pfuncs_o_u.extractSabishiDesu,
				'sabishidesu.tk'                                                       : pfuncs_o_u.extractSabishiDesu,
				'Sabishii desu!!'                                                      : pfuncs_o_u.extractSabishiidesu,
				'Sabishii-desu'                                                        : pfuncs_o_u.extractSabishiiDesu,
				'Saiaku Translations Blog'                                             : pfuncs_o_u.extractSaiakuTranslationsBlog,
				'SaiakuTranslationsblog'                                               : pfuncs_o_u.extractSaiakuTranslationsblog,
				'Saigo Translation'                                                    : pfuncs_o_u.extractSaigoTranslation,
				'Sakurane'                                                             : pfuncs_o_u.extractSakurane,
				'Sandwich Kingdom'                                                     : pfuncs_o_u.extractSandwichKingdom,
				'Sauri\'s TL Blog'                                                     : pfuncs_o_u.extractSaurisTLBlog,
				'Scanlating the Lodoss Novels'                                         : pfuncs_o_u.extractScanlatingTheLodossNovels,
				'Scarlet Madness'                                                      : pfuncs_o_u.extractScarletMadness,
				'Scrya Translations'                                                   : pfuncs_o_u.extractScryaTranslations,
				'Scum Bag Translation'                                                 : pfuncs_o_u.extractScumBagTranslation,
				'Secondo Korean'                                                       : pfuncs_o_u.extractSecondoKorean,
				'Segmeton Translation'                                                 : pfuncs_o_u.extractSegmetonTranslation,
				'Seikanji Ichizoku Translations'                                       : pfuncs_o_u.extractSeikanjiIchizokuTranslations,
				'Sekai no Kuroba'                                                      : pfuncs_o_u.extractSekainoKuroba,
				'Self Taught Japanese '                                                : pfuncs_o_u.extractSelfTaughtJapanese,
				'Selfish Translation'                                                  : pfuncs_o_u.extractSelfishTranslation,
				'Selkin Novel'                                                         : pfuncs_o_u.extractSelkinNovel,
				'SenjiQ creations'                                                     : pfuncs_o_u.extractSenjiQcreations,
				'Seonbi Novels'                                                        : pfuncs_o_u.extractSeonbiNovels,
				'Serene and Tranquil'                                                  : pfuncs_o_u.extractSereneandTranquil,
				'SETSUNA86BLOG'                                                        : pfuncs_o_u.extractSETSUNA86BLOG,
				'Shalvation Translations'                                              : pfuncs_o_u.extractShalvationTranslations,
				'Shameless Onii-san'                                                   : pfuncs_o_u.extractShamelessOniisan,
				'Sharramycats Translations'                                            : pfuncs_o_u.extractSharramycatsTranslations,
				'Shell2ly C-Novel Site'                                                : pfuncs_o_u.extractShell2lyCNovelSite,
				'Shen Yuan Lang MTL'                                                   : pfuncs_o_u.extractShenYuanLangMTL,
				'Sherma Translations'                                                  : pfuncs_o_u.extractShermaTranslations,
				'Shikkaku Translations'                                                : pfuncs_o_u.extractShikkakuTranslations,
				'Shin Sekai Yori – From the New World'                                 : pfuncs_o_u.extractShinSekaiYori,
				'Shin Translations'                                                    : pfuncs_o_u.extractShinTranslations,
				'Shine Translation'                                                    : pfuncs_o_u.extractShineTranslation,
				'Shinsori Translations'                                                : pfuncs_o_u.extractShinsori,
				'Shiro Translation'                                                    : pfuncs_o_u.extractShiroTranslation,
				'Shirohane'                                                            : pfuncs_o_u.extractShirohane,
				'Shiroyukineko Translations'                                           : pfuncs_o_u.extractShiroyukineko,
				'Shokyuu Translations'                                                 : pfuncs_o_u.extractShokyuuTranslations,
				'Shouldnt be here blog'                                                : pfuncs_o_u.extractShouldntbehereblog,
				'Shova Translations'                                                   : pfuncs_o_u.extractShovaTranslations,
				'Silent Tl'                                                            : pfuncs_o_u.extractSilentTl,
				'Silkpants Entente'                                                    : pfuncs_o_u.extractSilkpantsEntente,
				'Silva\'s Library'                                                     : pfuncs_o_u.extractSilvasLibrary,
				'Silver Butterfly'                                                     : pfuncs_o_u.extractSilverButterfly,
				'Sinister Translations'                                                : pfuncs_o_u.extractSinisterTranslations,
				'Sins of the Fathers'                                                  : pfuncs_o_u.extractSinsOfTheFathers,
				'Site Title'                                                           : pfuncs_o_u.extractSiteTitle,
				'Skull Squadron'                                                       : pfuncs_o_u.extractSkullSquadron,
				'Skythewood translations'                                              : pfuncs_o_u.extractSkythewood,
				'Slave Translations'                                                   : pfuncs_o_u.extractSlaveTranslations,
				'Sleepy Translations'                                                  : pfuncs_o_u.extractSleepyTranslations,
				'Slime Lv1'                                                            : pfuncs_o_u.extractSlimeLv1,
				'Sloth Translation'                                                    : pfuncs_o_u.extractSlothTranslation,
				'Sloth Translations Blog'                                              : pfuncs_o_u.extractSlothTranslationsBlog,
				'Sloth Translations'                                                   : pfuncs_o_u.extractSlothTranslations,
				'Snow & Dust'                                                          : pfuncs_o_u.extractSnowDust,
				'Snow Translations'                                                    : pfuncs_o_u.extractSnowTranslations,
				'SnowTime Translations'                                                : pfuncs_o_u.extractSnowTimeTranslations,
				'Snowy Publications'                                                   : pfuncs_o_u.extractSnowyPublications,
				'Soaring Translations'                                                 : pfuncs_o_u.extractSoaring,
				'Sod Translations'                                                     : pfuncs_o_u.extractSodTranslations,
				'Solitary Translation'                                                 : pfuncs_o_u.extractSolitaryTranslation,
				'Solstar24'                                                            : pfuncs_o_u.extractSolstar24,
				'Soltarination Scanlations'                                            : pfuncs_o_u.extractSoltarinationScanlations,
				'Soojiki\'s Project'                                                   : pfuncs_o_u.extractSoojikisProject,
				'Sooky\'s Kitchen'                                                     : pfuncs_o_u.extractSookySKitchen,
				'Sora Translations'                                                    : pfuncs_o_u.extractSoraTranslations,
				'Sora Translationsblog'                                                : pfuncs_o_u.extractSoraTranslations,
				'Soul Permutation'                                                     : pfuncs_o_u.extractSoulPermutation,
				'Sousetsuka'                                                           : pfuncs_o_u.extractSousetsuka,
				'SpaceforMemory'                                                       : pfuncs_o_u.extractSpaceforMemory,
				'Sparrowtranslations'                                                  : pfuncs_o_u.extractSparrowtranslations,
				'Spcnet.tv'                                                            : pfuncs_o_u.extractSpcnetTv,
				'Spirit God Shura'                                                     : pfuncs_o_u.extractSpiritGodShura,
				'Spirits Abound'                                                       : pfuncs_o_u.extractSpiritsAbound,
				'Spiritual Transcription'                                              : pfuncs_o_u.extractSpiritualTranscription,
				'Spring Scents'                                                        : pfuncs_o_u.extractSpringScents,
				'Starrydawn Translations'                                              : pfuncs_o_u.extractStarrydawnTranslations,
				'Startling Surprises at Every Step'                                    : pfuncs_o_u.extractStartlingSurprisesAtEveryStep,
				'StarveCleric'                                                         : pfuncs_o_u.extractStarveCleric,
				'Steadier Translations'                                                : pfuncs_o_u.extractSteadierTranslations,
				'Steady Translation'                                                   : pfuncs_o_u.extractSteadyTranslation,
				'Stellar Transformation Con.'                                          : pfuncs_o_u.extractStellarTransformationCon,
				'STL Translations'                                                     : pfuncs_o_u.extractSTLTranslations,
				'Stone Burners'                                                        : pfuncs_o_u.extractStoneBurners,
				'StrayCats'                                                            : pfuncs_o_u.extractStrayCats,
				'Subudai11'                                                            : pfuncs_o_u.extractSubudai11,
				'Suikoden I: Soul Eater Novel Translation'                             : pfuncs_o_u.extractSuikodenISoulEaterNovelTranslation,
				'Sun Shower Fields'                                                    : pfuncs_o_u.extractSunShowerFields,
				'SunnyTranslations'                                                    : pfuncs_o_u.extractSunnyTranslations,
				'Super Potato Translations'                                            : pfuncs_o_u.extractSuperPotatoTranslations,
				'SuperNyankoMofu~'                                                     : pfuncs_o_u.extractSuperNyankoMofu,
				'Supreme Origin Translations'                                          : pfuncs_o_u.extractSotranslations,
				'Suteki Da Ne'                                                         : pfuncs_o_u.extractSutekiDaNe,
				'Sweet A Collections'                                                  : pfuncs_o_u.extractSweetACollections,
				'Sword and Game'                                                       : pfuncs_o_u.extractSwordAndGame,
				'Sylver Translations'                                                  : pfuncs_o_u.extractSylver,
				'Symbiote'                                                             : pfuncs_o_u.extractSymbiote,
				'T&Q'                                                                  : pfuncs_o_u.extractTandQ,
				'Taida-dono Translations'                                              : pfuncs_o_u.extractTaidadonoTranslations,
				'Taint'                                                                : pfuncs_o_u.extractTaint,
				'Tales of MU'                                                          : pfuncs_o_u.extractTalesOfMU,
				'Tales of The Forgottenslayer'                                         : pfuncs_o_u.extractTalesofTheForgottenslayer,
				'tap-trans » tappity tappity tap.'                                     : pfuncs_o_u.extractTaptrans,
				'Tarable Translations'                                                 : pfuncs_o_u.extractTarableTranslations,
				'Tatakau Shisho Light Novel Translation'                               : pfuncs_o_u.extractTatakauShishoLightNovelTranslation,
				'tekuteku'                                                             : pfuncs_o_u.extractTekuteku,
				'Ten Thousand Heaven Controlling Sword'                                : pfuncs_o_u.extractTenThousandHeavenControllingSword,
				'Tensai Translations'                                                  : pfuncs_o_u.extractTensaiTranslations,
				'Tentatively under construction'                                       : pfuncs_o_u.extractTentativelyUnderconstruction,
				'Tequila Mockingbard'                                                  : pfuncs_o_u.extractTequilaMockingbard,
				'Terminus Translation'                                                 : pfuncs_o_u.extractTerminusTranslation,
				'ThatGuyOverThere'                                                     : pfuncs_o_u.extractThatGuyOverThere,
				'The Asian Cult'                                                       : pfuncs_o_u.extractTheAsianCult,
				'The Bathrobe Knight'                                                  : pfuncs_a_g.extractBathrobeKnight,
				'The Beginning After The End Novel'                                    : pfuncs_o_u.extractTheBeginningAfterTheEnd,
				'The Beginning After The End'                                          : pfuncs_a_g.extractBeginningAfterTheEnd,
				'The Bountiful REM Exploits of Danziger Monking'                       : pfuncs_o_u.extractTheBountifulRemExploitsOfDanzigerMonking,
				'The Boy Who Couldn\'t Be A Hero'                                      : pfuncs_o_u.extractTheBoyWhoCouldntBeAHero,
				'The C-Novel Project'                                                  : pfuncs_a_g.extractCNovelProj,
				'The Captain\'s Log'                                                   : pfuncs_o_u.extractTheCaptainSLog,
				'The Iron Teeth'                                                       : pfuncs_o_u.extractTheIronTeeth,
				'The Last Skull'                                                       : pfuncs_o_u.extractTheLastSkull,
				'The Lunacy of Duke Venomania'                                         : pfuncs_o_u.extractTheLunacyOfDukeVenomania,
				'The Mustang Translator'                                               : pfuncs_o_u.extractTheMustangTranslator,
				'The Named'                                                            : pfuncs_o_u.extractTheNamed,
				'The Other Half of My Apple'                                           : pfuncs_o_u.extractTheOtherHalfofMyApple,
				'The Place Closest to Heaven'                                          : pfuncs_o_u.extractThePlaceClosestToHeaven,
				'The Sphere'                                                           : pfuncs_o_u.extractTheSphere,
				'The Sun Is Cold Translations'                                         : pfuncs_o_u.extractTheSunIsColdTranslations,
				'The Tales of Paul Twister'                                            : pfuncs_o_u.extractTalesOfPaulTwister,
				'The Undying Cultivator'                                               : pfuncs_o_u.extractTheUndyingCultivator,
				'The Verbose Playground'                                               : pfuncs_o_u.extractTheVerbosePlayground,
				'The Viking Story Teller'                                              : pfuncs_o_u.extractTheVikingStoryTeller,
				'The World On The Other Side…'                                         : pfuncs_o_u.extractTheWorldOnTheOtherSide,
				'The Zombie Knight'                                                    : pfuncs_v_other.extractZombieKnight,
				'TheDefend Translations'                                               : pfuncs_o_u.extractTheDefendTranslations,
				'TheLazy9'                                                             : pfuncs_o_u.extractTheLazy9,
				'thepaperfictions.wordpress.com'                                       : pfuncs_o_u.extractThePaperFictions,
				'therabbitknight'                                                      : pfuncs_o_u.extractTherabbitknight,
				'This World Work'                                                      : pfuncs_o_u.extractThisWorldWork,
				'Throwaway'                                                            : pfuncs_o_u.extractThrowaway,
				'Thunder Translation'                                                  : pfuncs_o_u.extractThunder,
				'Thyaeria Translations'                                                : pfuncs_o_u.extractThyaeria,
				'Tieshaunn'                                                            : pfuncs_o_u.extractTieshaunn,
				'tiffybook.com'                                                        : pfuncs_a_g.extractCrazyForHENovels,
				'Timebun Translations'                                                 : pfuncs_o_u.extractTimebunTranslations,
				'Timeless MTL'                                                         : pfuncs_o_u.extractTimelessMtl,
				'Tinkerbell-san'                                                       : pfuncs_o_u.extractTinkerbellsan,
				'TL Syosetsu'                                                          : pfuncs_o_u.extractTLSyosetsu,
				'Toaaa~~~'                                                             : pfuncs_o_u.extractToaaa,
				'Tofubyu'                                                              : pfuncs_o_u.extractTofubyu,
				'Tokyo ESP Scans'                                                      : pfuncs_o_u.extractTokyoESPScans,
				'Tomorolls'                                                            : pfuncs_o_u.extractTomorolls,
				'Tony Yon Ka'                                                          : pfuncs_o_u.extractTonyYonKa,
				'Torii Translations'                                                   : pfuncs_o_u.extractToriiTranslations,
				'Totally Insane Tranlation'                                            : pfuncs_o_u.extractTotallyInsaneTranslation,
				'Totally Insane Translation'                                           : pfuncs_o_u.extractTotallyInsaneTranslation,
				'Totokk\'s Translations'                                               : pfuncs_o_u.extractTotokk,
				'Towards the Sky'                                                      : pfuncs_o_u.extractTowardstheSky,
				'Towards the Sky~'                                                     : pfuncs_o_u.extractTowardsTheSky,
				'Translated by a Clown'                                                : pfuncs_a_g.extractClownTrans,
				'Translated Novels Directory'                                          : pfuncs_o_u.extractTranslatedNovelsDirectory,
				'Translating For Your Pleasure'                                        : pfuncs_o_u.extractTranslatingForYourPleasure,
				'Translating Sloth'                                                    : pfuncs_o_u.extractTranslatingSloth,
				'Translating Ze Tian Ji'                                               : pfuncs_o_u.extractTranslatingZeTianJi,
				'Translating.Sloth'                                                    : pfuncs_o_u.extractTranslatingSloth,
				'Translation Nations'                                                  : pfuncs_o_u.extractTranslationNations,
				'Translation Raven'                                                    : pfuncs_o_u.extractTranslationRaven,
				'Translation Treasure Box'                                             : pfuncs_o_u.extractTranslationTreasureBox,
				'TranslationChicken'                                                   : pfuncs_o_u.extractTranslationchicken,
				'Translations From Outer Space'                                        : pfuncs_o_u.extractTranslationsFromOuterSpace,
				'Translator Eri'                                                       : pfuncs_o_u.extractTranslatorEri,
				'TresPasserby'                                                         : pfuncs_o_u.extractTrespasserby,
				'Trinity Archive'                                                      : pfuncs_o_u.extractTrinityArchive,
				'Tripp Translations'                                                   : pfuncs_o_u.extractTrippTl,
				'Trung Nguyen'                                                         : pfuncs_o_u.extractTrungNguyen,
				'Trungt Nguyen 123'                                                    : pfuncs_o_u.extractTrungtNguyen,
				'Try Translations'                                                     : pfuncs_o_u.extractTryTranslations,
				'TryTranslations/The Busy One'                                         : pfuncs_o_u.extractTryTranslationsTheBusyOne,
				'Tseirp Translations'                                                  : pfuncs_o_u.extractTseirpTranslations,
				'Tsubaki Translation'                                                  : pfuncs_o_u.extractTsubakiTranslation,
				'Tsuigeki Translations'                                                : pfuncs_o_u.extractTsuigeki,
				'Tsuki\'s Miscellaneous'                                               : pfuncs_o_u.extractTsukiSMiscellaneous,
				'Tsukigomori'                                                          : pfuncs_o_u.extractTsukigomori,
				'Ttukkirabit Translation'                                              : pfuncs_o_u.extractTtukkirabitTranslation,
				'Tumble Into Fantasy'                                                  : pfuncs_o_u.extractTumbleIntoFantasy,
				'Turb0 Translation'                                                    : pfuncs_o_u.extractTurb0,
				'Turtle and Hare Translations'                                         : pfuncs_o_u.extractTurtleandHareTranslations,
				'Turtle\'s'                                                            : pfuncs_o_u.extractTurtleS,
				'Tus-Trans'                                                            : pfuncs_o_u.extractTusTrans,
				'Twelve Months of May'                                                 : pfuncs_o_u.extractTwelveMonthsofMay,
				'Twig'                                                                 : pfuncs_o_u.extractTwig,
				'Twisted Cogs'                                                         : pfuncs_o_u.extractTwistedCogs,
				'Twki-san Otaku'                                                       : pfuncs_o_u.extractTwkisanOtaku,
				'Tynkerd'                                                              : pfuncs_o_u.extractTynkerd,
				'Tyrant\'s Eye Translations'                                           : pfuncs_o_u.extractTyrantsEyeTranslations,
				'U Donate We Translate'                                                : pfuncs_o_u.extractUDonateWeTranslate,
				'Ukel2x'                                                               : pfuncs_o_u.extractUkel2x,
				'Ultimaguil Base'                                                      : pfuncs_o_u.extractUltimaguilBase,
				'Ultimate Arcane'                                                      : pfuncs_o_u.extractUltimateArcane,
				'Unbreakable Machine Doll'                                             : pfuncs_o_u.extractUnbreakableMachineDoll,
				'Unchained Translation'                                                : pfuncs_o_u.extractUnchainedTranslation,
				'Undecent Translations'                                                : pfuncs_o_u.extractUndecentTranslations,
				'Unded Translations'                                                   : pfuncs_o_u.extractUndedTranslations,
				'UnicornsGalore!'                                                      : pfuncs_o_u.extractUnicornsGalore,
				'Unique Books'                                                         : pfuncs_o_u.extractUniqueBooks,
				'Universes With Meaning'                                               : pfuncs_o_u.extractUniversesWithMeaning,
				'Unlimited Novel Failures'                                             : pfuncs_o_u.extractUnlimitedNovelFailures,
				'Unlimited Story Works'                                                : pfuncs_o_u.extractUnlimitedStoryWorks,
				'Unnamed Translations'                                                 : pfuncs_o_u.extractUnnamedTranslations,
				'unnamedtranslations.blogspot.com'                                     : pfuncs_o_u.extractUnnamedtranslations,
				'Untuned Translation Blog'                                             : pfuncs_o_u.extractUntunedTranslation,
				'Useless no 4'                                                         : pfuncs_o_u.extractUselessno4,
				'v7 Silent'                                                            : pfuncs_v_other.extractV7Silent,
				'VaanCruze'                                                            : pfuncs_h_n.extractMaouTheYuusha,
				'Various Translated Work'                                              : pfuncs_v_other.extractVariousTranslatedWork,
				'Vee Translation'                                                      : pfuncs_v_other.extractVeeTranslation,
				'Verathragana Stories'                                                 : pfuncs_v_other.extractVerathragana,
				'Versatile Guy'                                                        : pfuncs_v_other.extractVersatileGuy,
				'VesperLxD Translation'                                                : pfuncs_v_other.extractVesperlxdTranslation,
				'VesperLxD'                                                            : pfuncs_v_other.extractVesperlxd,
				'Vestige Translations'                                                 : pfuncs_v_other.extractVestigeTranslations,
				'VgPerson'                                                             : pfuncs_v_other.extractVgperson,
				'Village Translations'                                                 : pfuncs_v_other.extractVillageTranslations,
				'Void Translations'                                                    : pfuncs_v_other.extractVoidTranslations,
				'Volare Novels'                                                        : pfuncs_v_other.extractVolareTranslations,   # So volare Translations apparently rebranded
				'Volare Translations'                                                  : pfuncs_v_other.extractVolareTranslations,
				'Walk the Jiang Hu'                                                    : pfuncs_v_other.extractWalkTheJiangHu,
				'Walking the Storm'                                                    : pfuncs_v_other.extractWalkingTheStorm,
				'Warrior Writing'                                                      : pfuncs_v_other.extractWarriorWriting,
				'Wat Da Meow'                                                          : pfuncs_v_other.extractWatDaMeow,
				'Watermelon Helmets'                                                   : pfuncs_v_other.extractWatermelonHelmets,
				'Wattpad'                                                              : pfuncs_v_other.extractWattpad,
				'WCC Translation'                                                      : pfuncs_v_other.extractWCCTranslation,
				'Weaboo Desu'                                                          : pfuncs_v_other.extractWeabooDesu,
				'Weaving stories and building castles in the clouds'                   : pfuncs_v_other.extractWeavingstoriesandbuildingcastlesintheclouds,
				'Web Novel Japanese Translation'                                       : pfuncs_v_other.extractWebNovelJapaneseTranslation,
				'weedsroyalroad'                                                       : pfuncs_v_other.extractWeedsroyalroad,
				'Welcome to the Malformed Box'                                         : pfuncs_v_other.extractWelcomeToTheMalformedBox,
				'Welcome To The Underdark'                                             : pfuncs_v_other.extractWelcomeToTheUnderdark,
				'Wele Translation'                                                     : pfuncs_v_other.extractWeleTranslation,
				'Wele Translations'                                                    : pfuncs_v_other.extractWeleTranslations,
				'Whatever Translations MTL'                                            : pfuncs_v_other.extractWhateverTranslationsMTL,
				'When The Hunting Party Came'                                          : pfuncs_v_other.extractWhenTheHuntingPartyCame,
				'Whimsical Land'                                                       : pfuncs_v_other.extractWhimsicalLand,
				'White Night Site'                                                     : pfuncs_v_other.extractWhiteNightSite,
				'White Tiger Translations'                                             : pfuncs_v_other.extractWhiteTigerTranslations,
				'Whiteleaf Tribe'                                                      : pfuncs_v_other.extractWhiteleafTribe,
				'Wiegenlied of Green'                                                  : pfuncs_v_other.extractWiegenliedOfGreen,
				'Wiggly Translation'                                                   : pfuncs_v_other.extractWigglyTranslation,
				'Willful Casual'                                                       : pfuncs_v_other.extractWillfulCasual,
				'Winter Translates'                                                    : pfuncs_v_other.extractWinterTranslates,
				'Wish Upon A Hope'                                                     : pfuncs_v_other.extractWishUponAHope,
				'Wisteria Translations'                                                : pfuncs_v_other.extractWisteriaTranslations,
				'Witch Life Novel'                                                     : pfuncs_v_other.extractWitchLife,
				'WL Translations'                                                      : pfuncs_v_other.extractWLTranslations,
				'Wolfie Translation'                                                   : pfuncs_v_other.extractWolfieTranslation,
				'Word of Craft'                                                        : pfuncs_v_other.extractWordofCraft,
				'Working NEET Translation'                                             : pfuncs_v_other.extractWorkingNEETTranslation,
				'Works of Kun'                                                         : pfuncs_v_other.extractWorksofKun,
				'World of Hope'                                                        : pfuncs_v_other.extractWorldofHope,
				'World of Summie'                                                      : pfuncs_v_other.extractWorldofSummie,
				'World of Watermelons'                                                 : pfuncs_v_other.extractWatermelons,
				'World Turtle Translations'                                            : pfuncs_v_other.extractWorldTurtleTranslations,
				'Worm - A Complete Web Serial'                                         : pfuncs_v_other.extractWormACompleteWebSerial,
				'Wums Translations'                                                    : pfuncs_v_other.extractWumsTranslations,
				'Wuwuwu555'                                                            : pfuncs_v_other.extractWuwuwu555,
				'Wuxia Fantasies'                                                      : pfuncs_v_other.extractWuxiaFantasies,
				'Wuxia Heroes'                                                         : pfuncs_v_other.extractWuxiaHeroes,
				'Wuxia Lovers'                                                         : pfuncs_v_other.extractWuxiaLovers,
				'Wuxia Translations'                                                   : pfuncs_v_other.extractWuxiaTranslations,
				'Wuxia Translators'                                                    : pfuncs_v_other.extractWuxiaTranslators,
				'Wuxia World'                                                          : pfuncs_v_other.extractWuxiaWorld,
				'WuxiaNation'                                                          : pfuncs_v_other.extractWuxiaNation,
				'WuxiaSociety'                                                         : pfuncs_v_other.extractWuxiaSociety,
				'Wuxiaworld'                                                           : pfuncs_v_other.extractWuxiaworld,
				'Wuxiwish'                                                             : pfuncs_v_other.extractWuxiwish,
				'www.nepustation.com'                                                  : pfuncs_v_other.extractNepustation,
				'www.pridesfamiliarsmaidens.com'                                       : pfuncs_o_u.extractPridesFamiliarsMaidens,
				'www.soltarination.org'                                                : pfuncs_o_u.extractSoltarination,
				'Xant & Minions'                                                       : pfuncs_v_other.extractXantAndMinions,
				'Xant Does Stuff and Things'                                           : pfuncs_v_other.extractXantDoesStuffAndThings,
				'xantbos.wordpress.com'                                                : pfuncs_v_other.extractXantbos,
				'XCrossJ Translations'                                                 : pfuncs_v_other.extractXcrossjTranslations,
				'XCrossJ'                                                              : pfuncs_v_other.extractXCrossJ,
				'Xiakeluojiao 侠客落脚'                                                    : pfuncs_v_other.extractXiakeluojiao侠客落脚,
				'Xian Foreigners'                                                      : pfuncs_v_other.extractXianForeigners,
				'Xian Xia World'                                                       : pfuncs_v_other.extractXianXiaWorld,
				'Xianxia Tales'                                                        : pfuncs_v_other.extractXianxiaTales,
				'Xiaoyuu\'s Translations'                                              : pfuncs_v_other.extractXiaoyuusTranslations,
				'Yamette Translations'                                                 : pfuncs_v_other.extractYametteTranslations,
				'Yami Translations'                                                    : pfuncs_v_other.extractYamiTranslations,
				'yamtl'                                                                : pfuncs_v_other.extractYamtl,
				'Yasashi Honyaku'                                                      : pfuncs_v_other.extractYasashiHonyaku,
				'Yeagdrasil'                                                           : pfuncs_v_other.extractYeagdrasil,
				'Yet Another Translation Site'                                         : pfuncs_h_n.extractMiaomix539,
				'Yi Yue Translation'                                                   : pfuncs_v_other.extractYiYueTranslation,
				'Yoraikun Translation'                                                 : pfuncs_v_other.extractYoraikun,
				'Yorasu Novels'                                                        : pfuncs_v_other.extractYorasuNovels,
				'Yorasu Translations'                                                  : pfuncs_v_other.extractYorasuTranslations,
				'Youjinsite Translations'                                              : pfuncs_v_other.extractYoujinsite,
				'Youko Advent'                                                         : pfuncs_v_other.extractYoukoAdvent,
				'Your Majesty Please Calm Down'                                        : pfuncs_v_other.extractYourMajestyPleaseCalmDown,
				'Youshoku Translations'                                                : pfuncs_v_other.extractYoushoku,
				'youtsubasilver\'s Blog'                                               : pfuncs_v_other.extractYoutsubasilversBlog,
				'Yukkuri Free Time Literature Service'                                 : pfuncs_v_other.extractYukkuri,
				'Yumeabyss'                                                            : pfuncs_v_other.extractYumeabyss,
				'yuNS Translations'                                                    : pfuncs_v_other.extractYuNSTranslations,
				'Yuujinchou'                                                           : pfuncs_v_other.extractYuujinchou,
				'Zaelum Translations'                                                  : pfuncs_v_other.extractZaelumTranslations,
				'ZAZA Translations'                                                    : pfuncs_v_other.extractZazaTranslations,
				'Zen Translations'                                                     : pfuncs_v_other.extractZenTranslations,
				'Zeonic'                                                               : pfuncs_v_other.extractZeonic,
				'Zero Translations'                                                    : pfuncs_v_other.extractZeroTranslations,
				'Zips_17'                                                              : pfuncs_v_other.extractZips_17,
				'Ziru\'s Musings | Translations~'                                      : pfuncs_v_other.extractZiruTranslations,
				'ZSW'                                                                  : pfuncs_v_other.extractZSW,
				'Zxzxzx\'s Blog'                                                       : pfuncs_v_other.extractZxzxzxSBlog,
				'~Taffy Translations~'                                                 : pfuncs_o_u.extractTaffyTranslations,
				'ℝeanとann@'                                                            : pfuncs_o_u.extractReantoAnna,
				'♥ yenney ♥'                                                           : pfuncs_v_other.extractYenney,
				'✱||| Straying away…。'                                                 : pfuncs_o_u.extractStrayingAway,
				'《不法之徒》 Lawless Gangster'                                              : pfuncs_v_other.extract不法之徒LawlessGangster,
				'「\u3000」'                                                             : pfuncs_o_u.extractU3000,
				'『書櫃』'                                                                 : pfuncs_v_other.extract書櫃,
				'お兄ちゃん、やめてぇ！'                                                          : pfuncs_o_u.extractOniichanyamete,
				'ヾ(。￣□￣)ﾂ'                                                             : pfuncs_a_g.extractAngry,
				'一期一会, 万歳!'                                                            : pfuncs_v_other.extract一期一会万歳,
				'中翻英圖書館 Translations'                                                  : pfuncs_o_u.extractTuShuGuan,
				'人见人爱的Sushi公主'                                                         : pfuncs_v_other.extract人见人爱的Sushi公主,
				'夢見る世界'                                                                : pfuncs_v_other.extract夢見る世界,
				'天才創造すなわち百合'                                                           : pfuncs_v_other.extract天才創造すなわち百合,
				'宿命の二人'                                                                : pfuncs_v_other.extract宿命の二人,
				'愛主の翻訳  Ainushi Translations'                                          : pfuncs_v_other.extract愛主の翻訳AinushiTranslations,
				'未完待续'                                                                 : pfuncs_v_other.extract未完待续,
				'桜翻訳! | Light novel translations'                                      : pfuncs_o_u.extractSakurahonyaku,
				'止めないで、お姉さま…'                                                          : pfuncs_v_other.extract止めないでお姉さま,
				'睡眠中毒'                                                                 : pfuncs_v_other.extract睡眠中毒,
				'輝く世界'                                                                 : pfuncs_v_other.extract輝く世界,
				'鏡像翻訳'                                                                 : pfuncs_v_other.extract鏡像翻訳,
				'閒人 • O N L I N E'                                                     : pfuncs_v_other.extract閒人ONLINE,
				'陽光的夏天'                                                                : pfuncs_v_other.extract陽光的夏天,
				'青玄豆腐幇'                                                                : pfuncs_v_other.extract青玄豆腐幇,
				'희노애락'                                                                 : pfuncs_v_other.extract희노애락,



				# Broken
				'Require: Cookie'                                                      : pfuncs_stub.extractNop,
				'Jun Cafe'                                                             : pfuncs_stub.extractNop,
				'Meteor Emperor-san'                                                   : pfuncs_stub.extractNop,
				'DuelNoir'                                                             : pfuncs_stub.extractNop,
				'Eternal Goddess Aria'                                                 : pfuncs_stub.extractNop,
				'An Unkie Musebox'                                                     : pfuncs_stub.extractNop,
				'Senpai Network'                                                       : pfuncs_stub.extractNop,
				'The Paper Fictions'                                                   : pfuncs_stub.extractNop,
				'Haruchika Novel'                                                      : pfuncs_stub.extractNop,
				'Re:Translations'                                                      : pfuncs_stub.extractNop,
				'Engrish Translation'                                                  : pfuncs_stub.extractNop,
				'Shibuya Psychic Research'                                             : pfuncs_stub.extractNop,
				'Nameless Translation'                                                 : pfuncs_stub.extractNop,


	}





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


		# ('Have Func', False), ('SourceName', 'sparklingdawnlights.blogspot.com'),

		# ('Have Func', False), ('SourceName', 'Zeonic'),
		# ('Have Func', False), ('SourceName', '「\u3000」'),
		# ('Have Func', False), ('SourceName', '天才創造すなわち百合'),

		# 'n00btranslations.wordpress.com'                                             : pfuncs.extractN00btranslations.wordpress.com,
		# 'omatranslations.wordpress.com'                                              : pfuncs.extractOmatranslations.wordpress.com,
		# 'soaringtranslations.wordpress.com'                                          : pfuncs.extractSoaringtranslations.wordpress.com,
		# 'solitarytranslation.wordpress.com'                                          : pfuncs.extractSolitarytranslation.wordpress.com,
		# 'walkthejianghu.wordpress.com'                                               : pfuncs.extractWalkthejianghu.wordpress.com,


		if item['srcname'] in RSS_PARSE_FUNCTION_MAP:
			try:
				ret = RSS_PARSE_FUNCTION_MAP[item['srcname']](item)
			except Exception as e:
				print("Failure when trying to extract item for source '%s'" % item['srcname'])
				print("srcname in map: ", item['srcname'] in RSS_PARSE_FUNCTION_MAP)
				if item['srcname'] in RSS_PARSE_FUNCTION_MAP:
					print("Value of `item['srcname'] in RSS_PARSE_FUNCTION_MAP`: ", RSS_PARSE_FUNCTION_MAP[item['srcname']])
				raise e
		else:
			print("No filter found for '%s'?" % item['srcname'])

		# NanoDesu is annoying and makes their releases basically impossible to parse. FFFUUUUUu
		if "(NanoDesu)" in item['srcname'] and not ret:
			return False

		if ret is None:
			return False

		bad_starts = [
			('FeedProxy', 'Comment on '),
			("Krytyk's Translations", 'By: '),
			('Prince Revolution!', 'By: '),
			('Blazing Translations', 'By: '),
			('Blazing Translations', 'Comment on '),
			('Aran Translations', 'Comment on '),

		]

		if (
				(flags.RSS_DEBUG or self.dbg_print)   and
				self.write_debug                      and
				ret is False                          and
				not "teaser" in item['title'].lower() and
				not "Preview" in item['tags']
			):
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if vol or chp or frag and not flags.RSS_DEBUG:

				if not any([(item['title'].startswith(bad) and item['srcname'] == src) for src, bad in bad_starts]):
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
							"Have Func"  : item['srcname'] in RSS_PARSE_FUNCTION_MAP,
						}

						# fp.write("\n==============================\n")
						# fp.write("Feed URL: '%s', guid: '%s'" % (item['linkUrl'], item['guid']))
						# fp.write("'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'\n" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix, item['linkUrl']))

						fp.write("%s" % (json.dumps(write_items, )))
						fp.write("\n")

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if self.dbg_print or flags.RSS_DEBUG:
			# False means not caught. None means intentionally ignored.

			if (
					ret is False         and
					(vol or chp or frag) and
					not "teaser" in item['title'].lower()
				):
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



		return ret


	def getProcessedReleaseInfo(self, feedDat):

		if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
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

		if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
			# print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return

		if any([feedDat['title'].lower().startswith(item) for item in common.global_constants.RSS_TITLE_FILTER]):
			# print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return


		# print("Feed item title: ", feedDat['title'], feedDat)

		if feedDat['title'].lower().startswith("by: "):
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

		try:
			new = self.getProcessedReleaseInfo(feedDat)
		except AssertionError:
			self.log.error("Exception when processing release!")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line.rstrip())

			return

		if tx_parse:
			if new:
				self.amqp_put_item(new)


		raw = self.getRawFeedMessage(feedDat)
		if tx_raw:
			if raw:
				self.amqp_put_item(raw)


def get_function_prefix(inn):
	nmap = {
		'a' : "pfuncs_a_g",
		'b' : "pfuncs_a_g",
		'c' : "pfuncs_a_g",
		'd' : "pfuncs_a_g",
		'e' : "pfuncs_a_g",
		'f' : "pfuncs_a_g",
		'g' : "pfuncs_a_g",

		'h' : "pfuncs_h_n",
		'i' : "pfuncs_h_n",
		'j' : "pfuncs_h_n",
		'k' : "pfuncs_h_n",
		'l' : "pfuncs_h_n",
		'm' : "pfuncs_h_n",
		'n' : "pfuncs_h_n",

		'o' : "pfuncs_o_u",
		'p' : "pfuncs_o_u",
		'q' : "pfuncs_o_u",
		'r' : "pfuncs_o_u",
		's' : "pfuncs_o_u",
		't' : "pfuncs_o_u",
		'u' : "pfuncs_o_u",
	}

	first_letter = fname_sanitize(inn)[0].lower()

	if first_letter in nmap:
		return nmap[first_letter]
	else:
		return "pfuncs_v_other"


def fname_sanitize(ins):

	# Largely empircally determined
	bad = r":'✱|…。()-:%.'\"!,★♥~?:&、<>"
	for badc in bad:
		ins = ins.replace(badc, "")

	while " " in ins:
		ins = ins.replace(" ", "")
	return ins

fmt_str = """
def %s(item):
	'''
	Parser for '%s'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False
	"""
def print_func_for_key(key):
	fkey = key.title().strip()


	fName = "extract{}".format(fname_sanitize(fkey))

	assert fName.isidentifier(), "'%s' is not a valid identifier (Base:'%s')" % (fName, key)

	func = fmt_str % (fName, key)

	with open("newfuncs.py", "a") as fp:
		fp.write("\n\n")
		fp.write(func)

	key = key.replace(r"'", r"\'")
	key = "'"+key+"'"

	return "				%s : %s.%s," % (key.ljust(70), get_function_prefix(key), fName)

def print_missing_functions():
	missing_cnt = 0
	ignored_cnt = 0

	with open("newfuncs.py", "w") as fp:
		fp.write("")

	items = [(key, val) for key, val in feedNameLut.mapper.items()]
	items = [val for key, val in items if key != val]
	items = list(set(items))
	items.sort(key=lambda x: fname_sanitize(x))

	name_map = []

	for value in items:
		if not value in RSS_PARSE_FUNCTION_MAP:
			missing_cnt += 1
			ret = print_func_for_key(value)
			name_map.append(ret)


	with open("newfuncs.py", "a") as fp:
		fp.write("\n\n")
		for item in name_map:

			fp.write(item + "\n")


	print("Missing %s out of %s items, %s ignored" % (missing_cnt, len(feedNameLut.mapper), ignored_cnt))