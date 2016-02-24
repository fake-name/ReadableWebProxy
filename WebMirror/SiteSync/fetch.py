

import WebMirror.util.webFunctions as webFunctions
import WebMirror.LogBase as LogBase
import WebMirror.rules
import urllib.parse
import urllib.error

class SiteSyncFetch(LogBase.LoggerMixin):


	def __init__(self):
		super().__init__()
		self.wg = webFunctions.WebGetRobust()
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


class AhoUpdatesFetch(SiteSyncFetch):

	loggerPath = "Main.AhoUpdatesFetcher"



	def getGroupSubpages(self):
		ret = []

		for x in range(500000):
			url = 'http://aho-updates.com/groups?sort_by=title&sort_order=ASC&page={num}'.format(num=x)

			try:
				soup = self.wg.getSoup(url)
			except urllib.error.URLError:
				break

			main = soup.find_all("div", class_='views-row')

			new = 0
			for item in [tmp for tmp in main if tmp.a]:
				url = item.a['href']
				if url.startswith("/group/"):
					url = urllib.parse.urljoin('http://aho-updates.com/', url)
					if url not in ret:
						ret.append(url)
						new += 1

			if new == 0:
				break

		self.log.info("Found %s group subpage URLs", len(ret))

		return ret

	def urlFromGroupPage(self, url):
		soup = self.wg.getSoup(url)
		content = soup.find('div', class_='field-name-field-lnu-grp-website')
		if not content:
			content = soup.find('span', class_='views-field-field-lnu-feed-main-url')
			if not content:
				raise ValueError("Wat?")
		if not content.a:
			raise ValueError("Wattt?")
		return content.a['href']

	def go(self):
		# print(self.urlFromGroupPage('http://aho-updates.com/group/dark-translations'))

		ret = []
		sp = self.getGroupSubpages()
		for p in sp:
			pg = self.urlFromGroupPage(p)
			if pg:
				ret.append(pg)
			self.log.info("Content page: %s", pg)
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


def fetch_other_sites():
	v1 = NovelUpdatesFetch.getGroupSites()
	v2 = AhoUpdatesFetch.getGroupSites()

	vals = v1+v2

	have = getExistingUrls()

	vals = set(vals)

	missed = []
	for val in vals:
		vloc = urllib.parse.urlsplit(val).netloc
		if not vloc in have:
			print("New: ", vloc)
			missed.append(vloc)
	with open("missed-urls.txt", "w") as fp:
		for miss in missed:
			fp.write("%s\n" % miss)

