
import itertools
import pprint

import common.LogBase
import common.util.WebRequest
import common.management.util



class WFGSeriesScraper(common.LogBase.LoggerMixin):
	loggerPath = 'Main.Wat'

	url_base = 'http://webfictionguide.com/'

	def __init__(self):
		super().__init__()

		self.wg = common.util.WebRequest.WebGetRobust()

	def get_intermediate_listing(self):
		ret = []

		for idx in itertools.count():

			url = "http://webfictionguide.com/online-novels/page/{page_num}/".format(page_num=idx)
			soup = self.wg.getSoup(url)

			content_div = soup.find("div", class_="listings")
			sdivs = content_div.find_all("div", class_="summary")

			self.log.info("Found %s series items on page (%s so far)", len(sdivs), len(ret))

			if not sdivs:
				break

			for sdiv in sdivs:
				linktag = sdiv.h3.a
				ret.append((linktag.get("href"), linktag.get_text(strip=True)))

		self.log.info("Found %s series", len(ret))
		return ret

	def resolve_actual_urls(self, s_page_url, s_title):
		self.log.info("Fetching actual URL for %s -> %s", s_title, s_page_url)

		soup = self.wg.getSoup(s_page_url)
		linkdiv = soup.find("div", class_="center")

		return s_title, common.management.util.get_page_title(self.wg, linkdiv.a.get("href"))


	def get_series(self):
		surls = self.get_intermediate_listing()

		for surl, stitle in surls:
			resp = self.resolve_actual_urls(surl, stitle)

			print("Site: ", resp)




def exposed_load_web_fiction_guide_stories():
	'''
	Scan the series on http://webfictionguide.com/, and
	fetch a list of the URLs for the series there.

	'''
	scraper = WFGSeriesScraper()
	scraper.get_series()

	# tmp = [
	# 	('http://webfictionguide.com/online-novels/and-the-skies-fell/',                      'And The Skies Fell'                     ),
	# 	('http://webfictionguide.com/online-novels/dark-blood/',                              'Dark Blood'                             ),
	# 	('http://webfictionguide.com/online-novels/constantchaotic/',                         'ConstantChaotic'                        ),
	# 	('http://webfictionguide.com/online-novels/the-shadows-of-sicily/',                   'The Shadows of Sicily'                  ),
	# 	('http://webfictionguide.com/online-novels/arrowhead-university/',                    'Arrowhead University'                   ),
	# 	('http://webfictionguide.com/online-novels/pale-and-gray/',                           'Pale And Gray'                          ),
	# 	('http://webfictionguide.com/online-novels/cold-iron/',                               'Cold Iron'                              ),
	# 	('http://webfictionguide.com/online-novels/void/',                                    'Void'                                   ),
	# 	('http://webfictionguide.com/online-novels/nowhere-town/',                            'Nowhere Town'                           ),
	# 	('http://webfictionguide.com/online-novels/the-bane-of-bennu/',                       'The Bane of Bennu'                      ),
	# 	('http://webfictionguide.com/online-novels/glamourist-extraordinaire/',               'Glamourist Extraordinaire'              ),
	# 	('http://webfictionguide.com/online-novels/the-misplaced-baroness/',                  'The Misplaced Baroness'                 ),
	# 	('http://webfictionguide.com/online-novels/strings-of-retaliation/',                  'Strings of Retaliation'                 ),
	# 	('http://webfictionguide.com/online-novels/vows-from-darkness/',                      'Vows From Darkness'                     ),
	# 	('http://webfictionguide.com/online-novels/shatterer-of-worlds/',                     'Shatterer of Worlds'                    ),
	# 	('http://webfictionguide.com/online-novels/the-finite-life-of-a-dating-sim-heroine/', 'The Finite Life of a Dating Sim Heroine'),
	# 	('http://webfictionguide.com/online-novels/bay-city-runaway/',                        'Bay City Runaway'                       ),
	# 	('http://webfictionguide.com/online-novels/the-fixers/',                              'The Fixers'                             ),
	# 	('http://webfictionguide.com/online-novels/kings-and-monsters/',                      'Kings and Monsters'                     ),
	# 	('http://webfictionguide.com/online-novels/the-mongolian-girl/',                      'The Mongolian Girl'                     ),
	# 	('http://webfictionguide.com/online-novels/athenas-iniquitous-gift/',                 'Athena’s Iniquitous Gift'               ),
	# 	('http://webfictionguide.com/online-novels/chronos-chronicles/',                      'Chronos Chronicles'                     ),
	# 	('http://webfictionguide.com/online-novels/book-of-the-blind/',                       'Book of the Blind'                      ),
	# 	('http://webfictionguide.com/online-novels/the-inuyama-rebellion/',                   'The Inuyama Rebellion'                  ),
	# 	('http://webfictionguide.com/online-novels/a-country-between/',                       'A Country Between'                      ),
	# 	('http://webfictionguide.com/online-novels/moondust/',                                'Moondust'                               ),
	# 	('http://webfictionguide.com/online-novels/becoming/',                                'Becoming'                               ),
	# 	('http://webfictionguide.com/online-novels/the-plot-to-end-all-plots/',               'The Plot to End All Plots'              )
	# ]

	# for surl, stitle in tmp:
	# 	resp = scraper.resolve_actual_urls(surl, stitle)
	# 	print(resp)

