



import bs4
import time
import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
from settings import WATTPAD_AUTH_CREDS


BAD_TOC_STR = \
'''	<div class="det-tab-pane" id="contents">
		<div class="g_wrap det-con mb30 j_catalog_wrap">
			<span class="g_loading _on"><i></i></span>
		</div>
	</div>'''

class QidianPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.Qidian"

	def get_csrf_tok(self):
		for cookie in self.wg.cj:
			if cookie.name == '_csrfToken':
				return cookie.value
		return None

	def get_chaps(self, url, book_id):
		csrf_tok = self.get_csrf_tok()
		if not csrf_tok:
			self.log.info("Forward-rendering page table-of-contents.")
			self.wg.getpage(url, returnMultiple=True)

			csrf_tok = self.get_csrf_tok()

		params = {
			'_csrfToken' : csrf_tok,
			'bookId'     : book_id,
			'_'          : str(int(time.time())),
		}
		toc_url = "https://www.webnovel.com/apiajax/chapter/GetChapterList?{}".format(urllib.parse.urlencode(params))

		toc_container = self.wg.getJson(toc_url)

		if (not 'msg' in toc_container
			or not 'data' in toc_container
			or not 'code' in toc_container
			or toc_container['msg'] != 'Success'
			or toc_container['code'] != 0
			):
			return

		toc_data = toc_container['data']
		if not 'chapterItems' in toc_data:
			return

		chapters = toc_data['chapterItems']
		chapters.sort(key=lambda x: x['chapterIndex'])

		return chapters

	def update_toc(self, url, soup):
		book_id = url.split("/")[-1].strip()

		chapters = self.get_chaps(url, book_id)
		if not chapters:
			return

		d_s = bs4.BeautifulSoup("<ul></ul>", "lxml")

		for chapter in chapters:
			linka           = d_s.new_tag("a")
			linka['id']     = "chapter-link"
			linka['href']   = "https://www.webnovel.com/book/{bid}/{cid}".format(bid=book_id, cid=chapter['chapterId'])
			linka.string    = "{} - {}".format(chapter['chapterIndex'], chapter['chapterName'])

			linkli = d_s.new_tag("li")
			linkli.append(linka)

			d_s.append(linkli)

		tocdiv = soup.find("div", id='contents')
		tocdiv.div.replace_with(d_s)


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)

		if BAD_TOC_STR in contentstr:
			content_soup = soup = bs4.BeautifulSoup(contentstr, "lxml")

			self.update_toc(url, content_soup)

			contentstr = content_soup.prettify()

		# if '<a id="header-item-login" rel="nofollow" href=' in contentstr:
		# 	self.log.info("Not logged into wattpad. Rectifying.")
		# 	contentstr = self.doLogin(contentstr, url)
		# 	self.log.info("Wattpad logged in.")
		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("www.webnovel.com")
