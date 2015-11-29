
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import json
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut



import WebMirror.OutputFilters.rss.ParserFuncs as pfuncs

from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import WebMirror.OutputFilters.FilterBase
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

				'1HP'                                       :  pfuncs.extract1HP,
				'87 Percent Translation'                    :  pfuncs.extract87Percent,
				'A fish once said this to me'               :  pfuncs.extractDarkFish,
				'AFlappyTeddyBird'                          :  pfuncs.extractAFlappyTeddyBird,
				'Alcsel Translations'                       :  pfuncs.extractAlcsel,
				'Alyschu & Co'                              :  pfuncs.extractAlyschuCo,
				'Ark Machine Translations'                  :  pfuncs.extractArkMachineTranslations,
				'AsherahBlue\'s Notebook'                   :  pfuncs.extractAsherahBlue,
				'Avert Translations'                        :  pfuncs.extractAvert,
				'Azure Sky Translation'                     :  pfuncs.extractAzureSky,
				'Baka Dogeza Translation'                   :  pfuncs.extractBakaDogeza,
				'Beehugger'                                 :  pfuncs.extractBeehugger,
				'Berseker Translations'                     :  pfuncs.extractBersekerTranslations,
				'Binggo&Corp'                               :  pfuncs.extractBinggoCorp,
				'Binhjamin'                                 :  pfuncs.extractBinhjamin,
				'Blue Silver Translations'                  :  pfuncs.extractBlueSilverTranslations,
				'Bu Bu Jing Xin Translation'                :  pfuncs.extractBuBuJingXinTrans,
				'Burei Dan Works'                           :  pfuncs.extractBureiDan,
				'C.E. Light Novel Translations'             :  pfuncs.extractCeLn,
				'Calico x Tabby'                            :  pfuncs.extractCalicoxTabby,
				'Clicky Click Translation'                  :  pfuncs.extractClicky,
				'Defiring'                                  :  pfuncs.extractDefiring,
				'DragomirCM'                                :  pfuncs.extractDragomirCM,
				'Dreadful Decoding'                         :  pfuncs.extractDreadfulDecoding,
				'Ensj Translations'                         :  pfuncs.extractEnsjTranslations,
				'EnTruce Translations'                      :  pfuncs.extractEnTruceTranslations,
				'Ero Light Novel Translations'              :  pfuncs.extractEroLightNovelTranslations,
				'Eros Workshop'                             :  pfuncs.extractErosWorkshop,
				'Fanatical'                                 :  pfuncs.extractFanatical,
				'FeedProxy'                                 :  pfuncs.extractFeedProxy,
				'Flower Bridge Too'                         :  pfuncs.extractFlowerBridgeToo,
				'Forgetful Dreamer'                         :  pfuncs.extractForgetfulDreamer,
				'Fudge Translations'                        :  pfuncs.extractFudgeTranslations,
				'Gila Translation Monster'                  :  pfuncs.extractGilaTranslation,
				'Giraffe Corps'                             :  pfuncs.extractGiraffe,
				'Gravity Tales'                             :  pfuncs.extractGravityTranslation,
				'guhehe.TRANSLATIONS'                       :  pfuncs.extractGuhehe,
				'Guro Translation'                          :  pfuncs.extractGuroTranslation,
				'Hajiko translation'                        :  pfuncs.extractHajiko,
				'Henouji Translation'                       :  pfuncs.extractHenoujiTranslation,
				'Hokage Translations'                       :  pfuncs.extractHokageTrans,
				'Imoutolicious Light Novel Translations'    :  pfuncs.extractImoutolicious,
				'Infinite Novel Translations'               :  pfuncs.extractInfiniteNovelTranslations,
				'Isekai Mahou Translations!'                :  pfuncs.extractIsekaiMahou,
				'Isekai Soul-Cyborg Translations'           :  pfuncs.extractIsekaiTranslation,
				'Iterations within a Thought-Eclipse'       :  pfuncs.extractIterations,
				'izra709 | B Group no Shounen Translations' :  pfuncs.extractIzra709,
				'Japtem'                                    :  pfuncs.extractJaptem,
				'JawzTranslations'                          :  pfuncs.extractJawzTranslations,
				'Kaezar Translations'                       :  pfuncs.extractKaezar,
				'Kerambit\'s Incisions'                     :  pfuncs.extractKerambit,
				'Kiri Leaves'                               :  pfuncs.extractKiri,
				'Kyakka'                                    :  pfuncs.extractKyakka,
				'Larvyde'                                   :  pfuncs.extractLarvyde,
				'Lazy NEET Translations'                    :  pfuncs.extractNEET,
				'Lingson\'s Translations'                   :  pfuncs.extractLingson,
				'Ln Addiction'                              :  pfuncs.extractLnAddiction,
				'Lunate'                                    :  pfuncs.extractLunate,
				'LygarTranslations'                         :  pfuncs.extractLygarTranslations,
				'MadoSpicy TL'                              :  pfuncs.extractMadoSpicy,
				'Mahou Koukoku'                             :  pfuncs.extractMahouKoukoku,
				'Mahoutsuki Translation'                    :  pfuncs.extractMahoutsuki,
				'Manga0205 Translations'                    :  pfuncs.extractManga0205Translations,
				'Mike777ac'                                 :  pfuncs.extractMike777ac,
				'Moon Bunny Cafe'                           :  pfuncs.extractMoonBunnyCafe,
				'Natsu TL'                                  :  pfuncs.extractNatsuTl,
				'NEET Translations'                         :  pfuncs.extractNeetTranslations,
				'Neo Translations'                          :  pfuncs.extractNeoTranslations,
				'Nightbreeze Translations'                  :  pfuncs.extractNightbreeze,
				'Nohohon Translation'                       :  pfuncs.extractNohohon,
				'NoviceTranslator'                          :  pfuncs.extractNoviceTranslator,
				'Ohanashimi'                                :  pfuncs.extractOhanashimi,
				'Omega Harem'                               :  pfuncs.extractOmegaHarem,
				'otterspacetranslation'                     :  pfuncs.extractOtterspaceTranslation,
				'Pika Translations'                         :  pfuncs.extractPikaTranslations,
				'putttytranslations'                        :  pfuncs.extractPuttty,
				'Raising the Dead'                          :  pfuncs.extractRaisingTheDead,
				'RANCER'                                    :  pfuncs.extractRancer,
				'Rebirth Online'                            :  pfuncs.extractRebirthOnline,
				'Rhinabolla'                                :  pfuncs.extractRhinabolla,
				'Rising Dragons Translation'                :  pfuncs.extractRisingDragons,
				'Ruze Translations'                         :  pfuncs.extractRuzeTranslations,
				'Scrya Translations'                        :  pfuncs.extractScryaTranslations,
				'Shikkaku Translations'                     :  pfuncs.extractShikkakuTranslations,
				'Shin Translations'                         :  pfuncs.extractShinTranslations,
				'Shiroyukineko Translations'                :  pfuncs.extractShiroyukineko,
				'Skythewood translations'                   :  pfuncs.extractSkythewood,
				'Sousetsuka'                                :  pfuncs.extractSousetsuka,
				'Supreme Origin Translations'               :  pfuncs.extractSotranslations,
				'Sword and Game'                            :  pfuncs.extractSwordAndGame,
				'Sylver Translations'                       :  pfuncs.extractSylver,
				'Tensai Translations'                       :  pfuncs.extractTensaiTranslations,
				'ThatGuyOverThere'                          :  pfuncs.extractThatGuyOverThere,
				'The C-Novel Project'                       :  pfuncs.extractCNovelProj,
				'TheLazy9'                                  :  pfuncs.extractTheLazy9,
				'Thunder Translation'                       :  pfuncs.extractThunder,
				'Tomorolls'                                 :  pfuncs.extractTomorolls,
				'Tony Yon Ka'                               :  pfuncs.extractTonyYonKa,
				'Totokk\'s Translations'                    :  pfuncs.extractTotokk,
				'Translated by a Clown'                     :  pfuncs.extractClownTrans,
				'Translation Nations'                       :  pfuncs.extractTranslationNations,
				'Tripp Translations'                        :  pfuncs.extractTrippTl,
				'Tsuigeki Translations'                     :  pfuncs.extractTsuigeki,
				'Turb0 Translation'                         :  pfuncs.extractTurb0,
				'Unchained Translation'                     :  pfuncs.extractUnchainedTranslation,
				'VaanCruze'                                 :  pfuncs.extractMaouTheYuusha,
				'Void Translations'                         :  pfuncs.extractVoidTranslations,
				'WCC Translation'                           :  pfuncs.extractWCCTranslation,
				'World of Watermelons'                      :  pfuncs.extractWatermelons,
				'Wuxia Translations'                        :  pfuncs.extractWuxiaTranslations,
				'Wuxiaworld'                                :  pfuncs.extractWuxiaworld,
				'Yoraikun Translation'                      :  pfuncs.extractYoraikun,
				'Yukkuri Free Time Literature Service'      :  pfuncs.extractYukkuri,
				'Ziru\'s Musings | Translations~'           :  pfuncs.extractZiruTranslations,
				'お兄ちゃん、やめてぇ！'                          :  pfuncs.extractOniichanyamete,
				'中翻英圖書館 Translations'                  :  pfuncs.extractTuShuGuan,
				'桜翻訳! | Light novel translations'        :  pfuncs.extractSakurahonyaku,

				'Lonahora'                                  :  pfuncs.extractLonahora,
				'WuxiaSociety'                              :  pfuncs.extractWuxiaSociety,
				'Wuxia Heroes'                              :  pfuncs.extractWuxiaHeroes,
				'Radiant Translations'                      :  pfuncs.extractRadiantTranslations,
				'Tales of MU'                               :  pfuncs.extractTalesOfMU,
				'ZSW'                                       :  pfuncs.extractZSW,

				'Youjinsite Translations'                   :  pfuncs.extractYoujinsite,
				'Youshoku Translations'                     :  pfuncs.extractYoushoku,
				'A0132'                                     :  pfuncs.extractA0132,
				'Lost in Translation'                       :  pfuncs.extractLostInTranslation,
				"Pea's Kingdom"                             :  pfuncs.extractPeasKingdom,
				'Circus Translations'                       :  pfuncs.extractCircusTranslations,
				'Distracted Translations'                   :  pfuncs.extractDistractedTranslations,
				'Forgotten Conqueror'                       :  pfuncs.extractForgottenConqueror,
				"Hold 'X' and Click"                        :  pfuncs.extractHoldX,
				'Hot Cocoa Translations'                    :  pfuncs.extractHotCocoa,
				'Solitary Translation'                      :  pfuncs.extractSolitaryTranslation,
				'A Place Of Legends'                        :  pfuncs.extractPlaceOfLegends,

				# KnW mess
				'Blazing Translations'                      :  pfuncs.extractKnW,
				'CapsUsingShift Tl'                         :  pfuncs.extractKnW,
				'Insignia Pierce'                           :  pfuncs.extractKnW,
				'Kiriko Translations'                       :  pfuncs.extractKnW,
				'Konjiki no Wordmaster'                     :  pfuncs.extractKnW,
				'Loliquent'                                 :  pfuncs.extractKnW,
				'Pummels Translations'                      :  pfuncs.extractKnW,
				'XCrossJ'                                   :  pfuncs.extractKnW,

				# Broken or not implemented yet
				'Untuned Translation Blog'                  :  pfuncs.extractBase,
				'Bad Translation'                           :  pfuncs.extractBase,
				'HaruPARTY'                                 :  pfuncs.extractBase,
				'Kami Translation'                          :  pfuncs.extractBase,
				'KobatoChanDaiSukiScan'                     :  pfuncs.extractBase,
				'LordofScrubs'                              :  pfuncs.extractBase,
				'Roasted Tea'                               :  pfuncs.extractBase,
				'Roxism HQ'                                 :  pfuncs.extractBase,
				'Shin Sekai Yori – From the New World'      :  pfuncs.extractBase,
				'Undecent Translations'                     :  pfuncs.extractBase,
				'ℝeanとann@'                                 :  pfuncs.extractBase,
				'pandafuqtranslations'                      :  pfuncs.extractBase,
				'Prince Revolution!'                        :  pfuncs.extractBase,
				'CtrlAlcalá'                                :  pfuncs.extractBase,
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
				# print("OK! '%s', V:'%s', C:'%s', '%s', '%s', '%s'" % (ret['srcname'], ret['vol'], ret['chp'], ret['postfix'], ret['series'], item['title']))
			else:
				pass
				# print("Wat: '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))

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
			return

		nicename = feedNameLut.getNiceName(feedDat['linkUrl'])
		if not nicename:
			nicename = urllib.parse.urlparse(feedDat['linkUrl']).netloc


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

