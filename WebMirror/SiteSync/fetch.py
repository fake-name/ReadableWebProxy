
import urllib.parse
import urllib.error

import common.util.WebRequest
import common.LogBase
import WebMirror.rules

class SiteSyncFetch(common.LogBase.LoggerMixin):


	def __init__(self):
		super().__init__()
		self.wg = common.util.WebRequest.WebGetRobust()
		self.log.info("Startup!")


	@classmethod
	def getGroupSites(cls):
		instance = cls()
		return instance.go()

class NovelUpdatesFetch(SiteSyncFetch):
	loggerPath = "Main.NovelUpdatesFetcher"

	def getGroupSubpages(self):
		ret = []

		for x in range(500000):
			url = 'http://www.novelupdates.com/groupslist/?pg={num}'.format(num=x)

			soup = self.wg.getSoup(url)
			main = soup.find("div", class_='g-cols')

			new = []
			for item in main.find_all("li"):
				if item.a:
					new.append(item.a['href'])
			if new:
				ret += new
			else:
				break

		self.log.info("Found %s group subpage URLs", len(ret))

		return ret

	def urlFromGroupPage(self, url):
		try:
			soup = self.wg.getSoup(url)
		except urllib.error.URLError:
			return None
		content = soup.find('div', class_='w-blog-content')
		if not content:
			raise ValueError("Wat?")
		rows = content.find_all('tr')
		for row in rows:
			tds = row.find_all("td")
			if len(tds) == 2:
				name, val = tds
				if name.get_text() == "URL":
					if val.a:
						return val.a['href']
					else:
						return None
		else:
			raise ValueError("Watt?")

	def go(self):
		# self.urlFromGroupPage('http://www.novelupdates.com/group/anon-empire/')

		ret = []
		sp = self.getGroupSubpages()
		for p in sp:
			pg = self.urlFromGroupPage(p)
			if pg:
				ret.append(pg)
			self.log.info("Content page: %s", pg)
		# 	pass
		# 	# print(p)
		return ret



def getExistingUrls():
	rules = WebMirror.rules.load_rules()

	netlocs = [item['starturls'] for item in rules if item['starturls']]
	netlocs = [list(set([urllib.parse.urlsplit(item).netloc for item in tmp])) for tmp in netlocs]

	[item.sort() for item in netlocs]

	ret = []
	for items in netlocs:
		ret += items
	print("Have %s existing urls!" % len(ret))
	return ret


# These are sites on (mostly) NovelUpdates that aren't actually
# valid sources. I think anyone can add anything, and there's some
# stupid shit.
bad_urls = [
	'cfensi.wordpress.com',                       # Chinese soap opera blog. Really?
	'chenguangsorchard.blogspot.com.au',          # More soap opera crap
	'koalasplayground.com',                       # Arrrrgh


	'creiz.livejournal.com',                      # Russian translations of a manga series.

	'www.fictionpress.com',                       # General fiction hosting site.
	'www.spcnet.tv',                              # General forum. Not a parseable single source.
	                                              # (I should really walk it at some point).
	'forum.wuxiaworld.com',                       # General forum. Not a parseable single source.
	'www.reddit.com',                             # Really?


	'messier-45.tumblr.com',                      # Translations of interviews with people
	'janeypeixes.tumblr.com',                     # Not the translations anymore.
	'agirlinjapan.tumblr.com',                    # Random garbage
	'lemoninagin.tumblr.com',                     # Moved

	'w-sensei.tumblr.com',                        # NFI
	'www.studentnotes.ca',                        # NFI
	'raspomme.tumblr.com',                        # NFI
	'fierydragonbreath.tumblr.com',               # NFI
	'cacatuasulphureacitrinocristata.tumblr.com', # Garbage naruto blog. Really?
	'trashbunny.tumblr.com',                      # Garbage

	'www.bhauth.com',                             # Some dude's random site. Literally nothing to do with LNs.
	'www.aresnovels.com',                         # Site is down.
	'tachibanachinatsu.wix.com',                  # Site is down.
	'blcxtranslations.github.io',                 # Site is down. Also github?
	'avertranslation.com',                        # Site is down.
	'minashiro.co.vu',                            # Removed, apparentlyaltoroctranslations.wordpress.com

	'daily-dallying.com',                         # Incorrect URL


	'hotchocolatescans.com',                      # Manga
	'www.ostnt.com',                              # Manga
	'www.world-three.org',                        # Manga
	'egscans.com',                                # Manga
	'riceballicious.info',                        # Manga
	'september.strawberrywine.org',               # BL Manga
	'mazuisubs.com',                              # Anime?


	'arestiny.com',                               # Appears to now be a domain squatter
	'www.noobtrans.ml',                           # Appears to now be a domain squatter

	'www.kudalakorn.com',                         # DNS NXDOMAIN
	'miracletranslations.azurewebsites.net',

	'www.wangkaiinternational.com',               # Blogger no longer found
	'springkrane.wixsite.com',
]


def fetch_other_sites():
	vals = NovelUpdatesFetch.getGroupSites()

	have = getExistingUrls()

	vals = set(vals)

	missed = []
	for val in vals:
		vloc = urllib.parse.urlsplit(val).netloc.lower()
		if vloc in bad_urls:
			continue

		if not vloc in have:
			print("New: ", vloc)
			missed.append(vloc)
	with open("missed-urls.txt", "w") as fp:
		for miss in missed:
			fp.write("%s\n" % miss)

