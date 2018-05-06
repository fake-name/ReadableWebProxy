



import bs4
import time
import WebMirror.PreProcessors.PreProcessorBase
import urllib.parse
from settings import WATTPAD_AUTH_CREDS


BAD_TOC_STR = \
'''<div class="det-tab-pane" id="contents">'''

'''	<div class="det-tab-pane" id="contents">
		<div class="g_wrap det-con mb30 j_catalog_wrap">
			<span class="g_loading _on"><i></i></span>
		</div>
	</div>'''

class QidianPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.Qidian"

	def get_csrf_tok(self):
		for cookie in self.wg_proxy().cj:
			if cookie.name == '_csrfToken':
				return cookie.value
		return None

	def get_chaps(self, url, book_id):
		csrf_tok = self.get_csrf_tok()
		if not csrf_tok:
			self.log.info("Forward-rendering page table-of-contents.")
			self.wg_proxy().getpage(url, returnMultiple=True)

			csrf_tok = self.get_csrf_tok()

		params = {
			'_csrfToken' : csrf_tok,
			'bookId'     : book_id,
			'_'          : str(int(time.time() * 1000)),
		}
		toc_url = "https://www.webnovel.com/apiajax/chapter/GetChapterList?{}".format(urllib.parse.urlencode(params))

		toc_container = self.wg_proxy().getJson(toc_url)

		if (not 'msg' in toc_container
			or not 'data' in toc_container
			or not 'code' in toc_container
			or toc_container['msg'] != 'Success'
			or toc_container['code'] != 0
			):
			self.log.error("API Call did not return success!")
			return

		toc_data = toc_container['data']
		if 'chapterItems' in toc_data:
			chapters = toc_data['chapterItems']
			chapters.sort(key=lambda x: x['index'])

			return chapters

		elif 'volumeItems' in toc_data:

			chapters = []
			for vol_num, vol_data in enumerate(toc_data['volumeItems']):
				vol_chapters = vol_data['chapterItems']
				for idx, chp in enumerate(vol_chapters):
					chp['chpIndex'] = (vol_num, idx)
					chapters.append(chp)
			chapters.sort(key=lambda x: x['index'])

			return chapters

		else:
			self.log.error("API Call response did not contain chapters")
			return


	def update_toc(self, url, soup):
		if "/book/" not in url:
			self.log.error("Not a book item?")
			return
		book_id = urllib.parse.urlsplit(url).path.split("/")[2]

		chapters = self.get_chaps(url, book_id)
		if not chapters:
			self.log.error("No chapters loaded! Nothing to do!")
			return

		main_list = bs4.BeautifulSoup("<div></div>", "lxml")


		self.log.info("ToC fetch found %s chapters!", len(chapters))

		d_s = main_list.new_tag("ul")
		for chapter in chapters:
			linka           = main_list.new_tag("a")
			linka['id']     = "chapter-link"
			linka['href']   = "https://www.webnovel.com/book/{bid}/{cid}".format(bid=book_id, cid=chapter['id'])
			linka.string    = "{} - {}".format(chapter['index'], chapter['name'])

			linkli = main_list.new_tag("li")
			linkli.append(linka)

			d_s.append(linkli)

		header = main_list.new_tag("h3")
		header.string = 'Table of Contents'
		main_list.append(header)
		main_list.append(d_s)

		tocdiv = soup.find("div", class_='j_tagWrap')
		tocdiv.insert_after(main_list)


	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)

		if BAD_TOC_STR in contentstr:
			self.log.info("Page %s may contain chapter placeholder. Fetching chapter ToC", url)
			content_soup = soup = bs4.BeautifulSoup(contentstr, "lxml")
			if content_soup.find("div", id='contents') and content_soup.find("div", id='contents').find('span', class_='g_loading'):
				self.log.info("Page %s contains chapter placeholder. Fetching chapter ToC", url)
				self.update_toc(url, content_soup)
				contentstr = content_soup.prettify()

		contentstr = contentstr.replace('<img src="//www.yueimg.com/en/images/common/imgPh.8c927.png" alt=" ">', "")

		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith("www.webnovel.com")
