


import WebMirror.PreProcessors.PreProcessorBase
import bs4
import re
import datetime
import markdown
import bbcode
import WebMirror.OutputFilters.FilterBase

def ago(then):
	if then == None:
		return "Never"
	now = datetime.datetime.now()
	delta = now - then

	d = delta.days
	h, s = divmod(delta.seconds, 3600)
	m, s = divmod(s, 60)
	labels = ['d', 'h', 'm', 's']
	dhms = ['%s %s' % (i, lbl) for i, lbl in zip([d, h, m, s], labels)]
	for start in range(len(dhms)):
		if not dhms[start].startswith('0'):
			break
	for end in range(len(dhms)-1, -1, -1):
		if not dhms[end].startswith('0'):
			break
	return ', '.join(dhms[start:end+1])


def build_item_summary(release_struct):
	d_s = bs4.BeautifulSoup("<b></b>", "lxml")
	tag = d_s.new_tag("div")

	header          = d_s.new_tag("h2")
	header.string   = release_struct['name']
	author          = d_s.new_tag("h4", id="series-author", author=release_struct['author_name'])
	author.string   = "By: " + release_struct['author_name']
	status          = d_s.new_tag("div")
	status.string   = "Status: " + str(release_struct['status'].title())
	chapters        = d_s.new_tag("h4")
	genres          = d_s.new_tag("div", id="series-genres",  genres=release_struct['genres'].strip(","))
	genres.string   = "Tags: " + release_struct['genres'].strip(",").replace(",", ", ")
	chapters.string = "Chapters: " + str(release_struct['chapters'])
	time            = d_s.new_tag("div", last_release = release_struct['last_update'])
	time.string     = "Last release: " + ago(datetime.datetime.fromtimestamp(int(release_struct['last_update'])))
	content         = d_s.new_tag("div")

	main = release_struct['description'].replace("\n", "<br>")
	main = markdown.markdown(main, extensions=["linkify"])
	for chunk in bs4.BeautifulSoup(main, "lxml").body:
		content.append(chunk)
	link            = d_s.new_tag("div")
	linka           = d_s.new_tag("a")
	linka['id']     = "rrl-series-link"
	linka['href']   = "http://royalroadl.com/fiction/{fid}".format(fid=release_struct['forum_id'])
	linka.string    = "Series Page"
	link.append(linka)

	t = d_s.new_tag("div")
	t.append(header)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(author)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(chapters)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(status)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(genres)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(time)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(content)
	tag.append(t)
	tag.append("\n")
	t = d_s.new_tag("div")
	t.append(link)
	tag.append(t)
	tag.append("\n")
	return tag


def build_bbcode_parser():
	def render_size(tag_name, value, options, parent, context):
		if 'size' in options:
			size = options['size']
		else:
			size = None
		if size == "medium":
			style = 'style="font-size: 150%"'
		elif size == "large":
			style = 'style="font-size: 200%"'
		elif size == "small":
			style = 'style="font-size: 75%"'
		else:
			style = ''
		return '<span %s>%s</span>' % (style, value)

	def render_font(tag_name, value, options, parent, context):
		if 'font' in options:
			font = options['font']
		else:
			font = None
		if font:
			style = "style='font:%s'" % font

		return '<span %s>%s</span>' % (style, value)

	parser = bbcode.Parser()
	parser.add_formatter('size', render_size)
	parser.add_formatter('font', render_font)
	parser.add_simple_formatter('table', '<table class="table-striped fullwidth">%(value)s</table>')
	parser.add_simple_formatter('tr',    '<tr>%(value)s</tr>')
	parser.add_simple_formatter('td',    '<td>%(value)s</td>')
	parser.add_simple_formatter('td1',   '<td>%(value)s</td>')
	parser.add_simple_formatter('td2',   '<td colspan="2">%(value)s</td>')
	parser.add_simple_formatter('td3',   '<td colspan="3">%(value)s</td>')
	parser.add_simple_formatter('td4',   '<td colspan="4">%(value)s</td>')

	return parser



class RRLListPagePreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.RoyalRoadL-Lists"


	URL_AJAX_KEYS = {
		"http://royalroadl.com/fictions/newest"            : "http://api.royalroadl.com/fictions.php?search=1&rpp=20&dir=DESC&page={pagenum}&status=&order_by=first_update",
		"http://royalroadl.com/fictions/popular-this-week" : "http://api.royalroadl.com/fictions.php?search=1&rpp=20&dir=DESC&page={pagenum}&status=&order_by=weekly",
		"http://royalroadl.com/fictions/best-rated"        : "http://api.royalroadl.com/fictions.php?search=1&rpp=20&dir=DESC&page={pagenum}&status=&order_by=",
		"http://royalroadl.com/fictions/latest-updates"    : "http://api.royalroadl.com/fictions.php?search=1&rpp=20&dir=DESClast_update&page={pagenum}&status=ONGOING&order_by=last_update",
		"http://royalroadl.com/fictions/active-only"       : "http://api.royalroadl.com/fictions.php?search=1&rpp=20&dir=DESC&page={pagenum}&status=ONGOING&order_by=",
	}


	def build_proper_page(self, url, contentstr):
		posts = []
		for x in range(3):
			ctnt = self.wg.getJson(self.URL_AJAX_KEYS[url].format(pagenum = x))
			posts.extend(ctnt)

		soup = bs4.BeautifulSoup(contentstr, "lxml")

		postlist = soup.new_tag("ul")


		for release in posts:
			post = build_item_summary(release)
			t = soup.new_tag("div")
			t.append(post)
			postlist.append(t)

		soup.find("md-content").clear()
		soup.find("md-content").append(postlist)

		return soup.prettify()

	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr

		if url in self.URL_AJAX_KEYS:
			contentstr = self.build_proper_page(url, contentstr)

		self.log.info("Preprocessing content from URL: '%s'", url)

		return contentstr


	@staticmethod
	def wantsUrl(url):
		return "http://royalroadl.com/fictions/" in url.lower() or "https://royalroadl.com/fictions/" in url.lower()

class RRLSeriesPagePreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.RoyalRoadL-Series"

	def build_chapter_list(self, chapters_json, fid):

		d_s = bs4.BeautifulSoup("<b></b>", "lxml")
		release = d_s.new_tag("ul")

		#
		for chapter in chapters_json:
			tag = d_s.new_tag("li")
			chpurl = "http://royalroadl.com/fiction/{fid}/chapter/{cid}".format(fid=fid, cid=chapter['tid'])
			chp          = d_s.new_tag("a", href=chpurl)
			chp.string   = chapter['subject']

			tag.append(chp)
			tag.append("\n")
			release.append(tag)

		return release

	def get_volume_tuples(self, volume_json):
		ret = []
		for volumeset in volume_json:
			print(volumeset)
			ret.append((volumeset['id'], volumeset['volume_name']))
		return ret

	def build_proper_page(self, url, contentstr):
		soup = bs4.BeautifulSoup(contentstr, "lxml")

		fid = url.split("/")[-1]

		release_info = self.wg.getJson("http://api.royalroadl.com/fictions.php?fid={fid}".format(fid = fid))
		volume_json      = self.wg.getJson("http://api.royalroadl.com/chapters.php?action=volumes&fid={fid}".format(fid = fid))


		postlist = soup.new_tag("div")

		post     = build_item_summary(release_info)
		postlist.append(post)

		volumes = [
			("null", ""),
			]
		volumes.extend(self.get_volume_tuples(volume_json))
		for vid, volname in volumes:
			chapters = self.wg.getJson("http://api.royalroadl.com/chapters.php?action=volumeChapters&volume={vid}&fid={fid}".format(fid = fid, vid=vid))
			chapters = self.build_chapter_list(chapters, release_info['forum_id'])
			if volname:

				item = soup.new_tag("div")
				b = soup.new_tag("b")
				b.string = volname
				item.append(b)
				postlist.append(item)
			postlist.append(chapters)

		# print(postlist)
		soup.find("md-content").clear()
		soup.find("md-content").append(postlist)

		ret = soup.prettify()
		# print(ret)
		return ret

	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr

		self.log.info("Preprocessing content from URL: '%s'", url)
		contentstr = self.build_proper_page(url, contentstr)

		return contentstr


	@staticmethod
	def wantsUrl(url):
		release = re.match(r'^http://royalroadl.com/fiction/\d+$', url)
		print("[RRLSeriesPagePreprocessor] - WantsURL: Release = ", release)
		return bool(release)

class RRLChapterPagePreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.RoyalRoadL-Chapter"

	def build_item_page(self, fid, chapter_struct):
		d_s = bs4.BeautifulSoup("<b></b>", "lxml")
		tag = d_s.new_tag("div")

		title          = d_s.new_tag("h2")
		title.string   = chapter_struct['title']

		author          = d_s.new_tag("h4")
		author.string   = "By: " + chapter_struct['chapterAuthor']

		time            = d_s.new_tag("div")
		time.string     = "Last release: " + ago(datetime.datetime.fromtimestamp(int(chapter_struct['dateline'])))

		content         = d_s.new_tag("div")

		main = chapter_struct['content']
		parser = build_bbcode_parser()
		main = parser.format(main)
		for chunk in bs4.BeautifulSoup(main, "lxml").body:
			content.append(chunk)

		link            = d_s.new_tag("div")
		linka           = d_s.new_tag("a")
		linka['id']     = "rrl-series-link"
		linka['href']   = "http://royalroadl.com/fiction/{fid}".format(fid=fid)
		linka.string    = "Series Page"
		link.append(linka)

		t = d_s.new_tag("div")
		t.append(title)
		tag.append(t)
		tag.append("\n")
		t = d_s.new_tag("div")
		t.append(author)
		tag.append(t)
		tag.append("\n")
		t = d_s.new_tag("div")
		t.append(time)
		tag.append(t)
		tag.append("\n")
		t = d_s.new_tag("div")
		t.append(content)
		tag.append(t)
		tag.append("\n")
		t = d_s.new_tag("div")
		t.append(link)
		tag.append(t)
		tag.append("\n")
		return tag



	def build_proper_page(self, dummy_url, fid, sid):
		soup = bs4.BeautifulSoup("", "lxml")

		release_info  = self.wg.getJson("http://api.royalroadl.com/fiction_chapters.php?fid={fid}&tid={sid}".format(fid=fid, sid=sid))
		adjacent_info = self.wg.getJson("http://api.royalroadl.com/fiction_chapters.php?action=getNavChapter&tid={sid}".format(fid=fid, sid=sid))

		postlist = soup.new_tag("div")

		post     = self.build_item_page(fid, release_info)
		postlist.append(post)

		soup.append(postlist)

		ret = soup.prettify()
		# print(ret)
		return ret

	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr

		release = re.match(r'^https?://w?w?w?\.?royalroadl.com/fiction/([\d]+)[\d\-a-z]*?/chapter/([\d]+)[\d\-a-z]*?$', url)
		if not release:
			raise ValueError("Wat?")
		print(release.groups())

		self.log.info("Preprocessing content from URL: '%s'", url)
		contentstr = self.build_proper_page(url, release.groups()[0], release.groups()[1])

		return contentstr


	@staticmethod
	def wantsUrl(url):
		release = re.match(r'^https?://w?w?w?\.?royalroadl.com/fiction/[\d\-a-z]+/chapter/[\d\-a-z]+$', url)
		return bool(release)
