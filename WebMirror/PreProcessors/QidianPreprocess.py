



import time
import ast
import json
import urllib.parse
import parsedatetime

import bs4
import common.get_rpyc

from WebMirror.OutputFilters.util.MessageConstructors import fix_string
from WebMirror.OutputFilters.util.MessageConstructors import createReleasePacket
from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseDeleteMessageWithType
from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessageWithType
import WebMirror.PreProcessors.PreProcessorBase


BAD_TOC_STR = '''<div class="det-tab-pane" id="contents">'''

CHAP_LOADER_STR = '''<div class="iso-area j_chapterLoading cha-loader">'''

'''	<div class="det-tab-pane" id="contents">
		<div class="g_wrap det-con mb30 j_catalog_wrap">
			<span class="g_loading _on"><i></i></span>
		</div>
	</div>'''

class QidianPreprocessor(WebMirror.PreProcessors.PreProcessorBase.ContentPreprocessor):

	loggerPath = "Main.Preprocessor.Qidian"

	# Lazy-load the remote interface construction.
	def __getattr__(self, name):
		if name == "rpc_interface" and not name in self.__dict__:
			self.rpc_interface = common.get_rpyc.RemoteJobInterface("FeedUpdater")
			self.rpc_interface.check_ok()
			return self.rpc_interface

		else:
			raise AttributeError

	def __del__(self):
		if hasattr(self, "rpc_interface"):
			self.rpc_interface.close()


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
		book_data = toc_data.get('bookInfo', {})

		if 'chapterItems' in toc_data:
			chapters = toc_data['chapterItems']
			chapters.sort(key=lambda x: x['index'])

			return book_data, chapters

		elif 'volumeItems' in toc_data:

			chapters = []
			for vol_num, vol_data in enumerate(toc_data['volumeItems']):
				vol_chapters = vol_data['chapterItems']
				for idx, chp in enumerate(vol_chapters):
					chp['chpIndex'] = (vol_num, idx)
					chapters.append(chp)
			chapters.sort(key=lambda x: x['index'])

			return book_data, chapters

		else:
			self.log.error("API Call response did not contain chapters")
			return None, None


	def do_release_for_chap(self, book_data, chap_info):


		itemDate, status = parsedatetime.Calendar().parse(chap_info['createTime'])

		if status < 1:
			self.log.warning("Failed to process release date info: '%s'", chap_info['createTime'])
			return

		reldate = time.mktime(itemDate)

		fake_raw_1 = {
			'srcname'   : "Qidian",
			'published' : reldate,
			'linkUrl'   : "https://www.webnovel.com/book/{book_id}/{chap_id}/".format(
				book_id = book_data['bookId'], chap_id = chap_info['id']),
		}


		fake_raw_2 = {
			'srcname'   : "Qidian",
			'published' : reldate,
			'linkUrl'   : "https://www.webnovel.com/rssbook/{book_id}/{chap_id}/".format(
				book_id = book_data['bookId'], chap_id = chap_info['id']),
		}


		if chap_info['isVip'] == 0:
			msg_1 = buildReleaseMessageWithType(
					raw_item    = fake_raw_1,
					series      = book_data['bookName'],
					vol         = None,
					chap        = chap_info['index'],
					frag        = None,
					postfix     = chap_info['name'],
					tl_type     = 'translated' if book_data['original'] is False else 'oel',
					looseMatch  = True,
					prefixMatch = True,
				)

			msg_2 = buildReleaseDeleteMessageWithType(
					raw_item    = fake_raw_2,
					series      = book_data['bookName'],
					vol         = None,
					chap        = chap_info['index'],
					frag        = None,
					postfix     = chap_info['name'],
					tl_type     = 'translated' if book_data['original'] is False else 'oel',
					looseMatch  = True,
					prefixMatch = True,
				)

			# print("release message:", msg)
			disp_1 = json.dumps(msg_1)
			self.rpc_interface.put_feed_job(disp_1)

			disp_2 = json.dumps(msg_2)
			self.rpc_interface.put_feed_job(disp_2)

		else:
			msg_1 = buildReleaseDeleteMessageWithType(
					raw_item    = fake_raw_1,
					series      = book_data['bookName'],
					vol         = None,
					chap        = chap_info['index'],
					frag        = None,
					postfix     = chap_info['name'],
					tl_type     = 'translated' if book_data['original'] is False else 'oel',
					looseMatch  = True,
					prefixMatch = True,
				)
			msg_2 = buildReleaseDeleteMessageWithType(
					raw_item    = fake_raw_2,
					series      = book_data['bookName'],
					vol         = None,
					chap        = chap_info['index'],
					frag        = None,
					postfix     = chap_info['name'],
					tl_type     = 'translated' if book_data['original'] is False else 'oel',
					looseMatch  = True,
					prefixMatch = True,
				)
			# print("release message:", msg)
			disp_1 = json.dumps(msg_1)
			self.rpc_interface.put_feed_job(disp_1)

			disp_2 = json.dumps(msg_2)
			self.rpc_interface.put_feed_job(disp_2)






	def update_toc(self, url, soup):
		if "/book/" not in url:
			self.log.error("Not a book item?")
			return
		book_id = urllib.parse.urlsplit(url).path.split("/")[2]

		book_data, chapters = self.get_chaps(url, book_id)
		if not chapters:
			self.log.error("No chapters loaded! Nothing to do!")
			return

		main_list = bs4.BeautifulSoup("<div></div>", "lxml")

		book_data['original'] = False

		if soup.find("strong", class_='z1'):
			if 'original' in soup.find("strong", class_='z1').get_text(strip=True):
				self.log.info("Series is original!")
				book_data['original'] = True


		self.log.info("ToC fetch found %s chapters!", len(chapters))

		d_s = main_list.new_tag("ul")
		for chapter in chapters:
			linka           = main_list.new_tag("a")
			linka['class']  = "chapter-link"
			linka['id']     = "chapter-link"
			linka['href']   = "https://www.webnovel.com/book/{bid}/{cid}".format(bid=book_id, cid=chapter['id'])
			linka.string    = "{}{} ({}) - {}".format(
				"BULLSHIT LOCKED - " if chapter['isVip'] else "",
				chapter['chpIndex'],
				chapter['index'],
				chapter['name'])
			linka['data-preprocessor-state']   = chapter['isVip']
			linka['data-preprocessor-vol']     = chapter['chpIndex'][0]
			linka['data-preprocessor-chp']     = chapter['chpIndex'][1]
			linka['data-preprocessor-name']    = chapter['name']
			linka['data-preprocessor-index']   = chapter['index']
			linka['data-preprocessor-title']   = book_data['bookName']
			linka['data-preprocessor-reldate'] = chapter['createTime']


			self.do_release_for_chap(book_data, chapter)

			linkli = main_list.new_tag("li")
			linkli.append(linka)

			d_s.append(linkli)

		header = main_list.new_tag("h3")
		header.string = 'Table of Contents'
		main_list.append(header)
		main_list.append(d_s)


		tocdiv = soup.find("div", class_='j_tagWrap')
		tocdiv.insert_after(main_list)

	def extract_chapinfo_segment(self, soup):
		for script_tag in soup.find_all('script'):
			script = script_tag.get_text()
			if 'var chapInfo = ' in script:
				lines = script.split("\n")
				val_lines = [tmp.strip() for tmp in lines if 'var chapInfo = ' in tmp]
				if len(val_lines) == 1:
					chapinfo = val_lines[0]
					_, chapinfo = chapinfo.split("=", 1)
					chapinfo = chapinfo.rstrip(";")
					chapinfo = chapinfo.replace(":null", ":None")
					chapinfo = chapinfo.strip()

					return ast.literal_eval(chapinfo)

	def insert_nav(self, url, soup, chapinfo):

		next_ch_id = str(chapinfo['chapterInfo']['nextChapterId'])
		prev_ch_id = str(chapinfo['chapterInfo']['preChapterId'])

		link_root = url
		while link_root.count("/") > 4:
			link_root, _ = link_root.rsplit("/", 1)

		link_root += "/"

		for ps_garb_div in soup.find_all('div', class_='cha-bts'):
			ps_garb_div.attrs = None
			ps_garb_div.clear()

			if prev_ch_id == "-1" or prev_ch_id == -1:
				prev_chp_tag = soup.new_tag('span')
			else:
				prev_chp_tag = soup.new_tag('a', href=link_root + prev_ch_id + "/")

			if next_ch_id == "-1" or next_ch_id == -1:
				next_chp_tag = soup.new_tag('span')
			else:
				next_chp_tag = soup.new_tag('a', href=link_root + next_ch_id + "/")

			toc_chp_tag = soup.new_tag('a', href=link_root)

			prev_chp_tag.attrs['style'] = 'float: left'
			next_chp_tag.attrs['style'] = 'float: right'

			prev_chp_tag.string = "Previous Chapter"
			toc_chp_tag.string  = "Table of Contents"
			next_chp_tag.string = "Next Chapter"

			ps_garb_div.append(prev_chp_tag)
			ps_garb_div.append(" ")
			ps_garb_div.append(toc_chp_tag)
			ps_garb_div.append(" ")
			ps_garb_div.append(next_chp_tag)


		return soup.prettify()

	def add_chap_nav_links(self, url, contentstr):
		content_soup = bs4.BeautifulSoup(contentstr, "lxml")

		chapinfo = self.extract_chapinfo_segment(content_soup)


		if 'chapterInfo' in chapinfo and 'nextChapterId' in chapinfo['chapterInfo'] and 'preChapterId' in chapinfo['chapterInfo']:
			contentstr = self.insert_nav(url, content_soup, chapinfo)


		return contentstr

	def preprocessContent(self, url, mimetype, contentstr):
		if not isinstance(contentstr, str):
			return contentstr
		self.log.info("Preprocessing content from URL: '%s'", url)

		if BAD_TOC_STR in contentstr:
			self.log.info("Page %s may contain chapter placeholder. Fetching chapter ToC", url)
			content_soup = bs4.BeautifulSoup(contentstr, "lxml")
			if content_soup.find("div", id='contents') and content_soup.find("div", id='contents').find('span', class_='g_loading'):
				self.log.info("Page %s contains chapter placeholder. Fetching chapter ToC", url)
				self.update_toc(url, content_soup)
				contentstr = content_soup.prettify()

		if CHAP_LOADER_STR in contentstr:
			self.log.info("Page %s seems to be a chapter page. Adding navigation links.", url)
			contentstr = self.add_chap_nav_links(url, contentstr)

		contentstr = contentstr.replace('<img src="//www.yueimg.com/en/images/common/imgPh.8c927.png" alt=" ">', "")

		return contentstr

	@staticmethod
	def wantsUrl(url):
		netloc = urllib.parse.urlsplit(url).netloc
		return netloc.lower().endswith(".webnovel.com")
ast