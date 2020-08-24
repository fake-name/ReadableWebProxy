
import datetime
import traceback
import pprint
import logging


import tqdm
import WebRequest

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()



import common.database as db
from WebMirror.processor.RssProcessor import RssProcessor
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix


log = logging.getLogger("Main.Manage.CrNManage")

def exposed_crn_series_type_from_chapter_url(url):
	'''
	Given a chapter url on crn, get the series name.

	Mostly exposed for debugging, it's used by (exposed_)process_new_fb.
	'''
	wg = WebRequest.WebGetRobust()

	soup = wg.getSoup(url)
	surl_tag = soup.find("a", class_='title_search')
	assert surl_tag

	surl = surl_tag['href']
	sname = surl_tag.get_text(strip=True)

	log.info("Series page URL: '%s'", surl)
	log.info("Series name: '%s'", sname)

	spage = wg.getSoup(surl)


	author_div = spage.find("div", class_='e45344-16')
	assert author_div

	auth_href = author_div.a

	auth_div_str = author_div.get_text(strip=True).lower()

	if   "translator:" in auth_div_str and "author:" in auth_div_str:
		log.info("Inferred series type: Translated")
		return sname, "translated"
	elif "author:" in auth_div_str:
		log.info("Inferred series type: OEL")
		return sname, "oel"
	else:
		raise RuntimeError("Unknown series type for item: '%s' with series page '%s' (%s)" % (url, surl, auth_div_str) )



def process_release(dp, proc_tmp, titlestr):
	proc_tmp['vcfp']      = extractVolChapterFragmentPostfix(titlestr)
	return dp.dispatchReleaseDbBacked(proc_tmp)

def proto_process_releases(sess, feed_releases):
	ret_dict = {
			"successful" : [],
			"missed"     : [],
			"ignored"    : [],
			"ignored-w-tumblr-idiots"    : [],
	}

	feed_releases = list(feed_releases)
	feed_releases.sort(key=lambda x: x.published, reverse=True)

	print("Found %s feed releases" % len(feed_releases))
	dp = RssProcessor(
			db_sess=sess,
			loggerPath="Main.WebProto",
			pageUrl=None,
			pgContent=None,
			type=None,
			)

	futures = []

	for item in tqdm.tqdm(feed_releases):

		proc_tmp = {}
		proc_tmp['feedtype']  = item.type
		proc_tmp['title']     = item.title
		proc_tmp['guid']      = item.contentid
		proc_tmp['linkUrl']   = item.contenturl
		proc_tmp['updated']   = item.updated
		proc_tmp['published'] = item.published
		proc_tmp['contents']  = item.contents
		proc_tmp['tags']      = item.tags
		proc_tmp['authors']   = item.author
		proc_tmp['srcname']   = item.feed_entry.feed_name
		proc_tmp['feed_id']   = item.feed_entry.id

		# proc_tmp['vcfp']      = extractVolChapterFragmentPostfix(item.title)
		future_tbd = process_release(dp, proc_tmp, str(item.title))
		futures.append((future_tbd, proc_tmp))

	for ret, proc_tmp in futures:
		# False means not caught. None means intentionally ignored.
		if ret:
			ret_dict["successful"].append((ret, proc_tmp))
		elif ret is False:
			ret_dict["missed"].append((ret, proc_tmp))
		elif ret is None:
			if 'tumblr.com/' not in proc_tmp['linkUrl']:
				ret_dict["ignored"].append((ret, proc_tmp))
			ret_dict["ignored-w-tumblr-idiots"].append((ret, proc_tmp))

		else:
			raise RuntimeError("Wat? Unknown ret ({}) for release: {}".format(ret, proc_tmp))

	return ret_dict


def exposed_crn_new_series(fetch_title=False):
	'''
	Process items from Creative Novels/Fantasy-Books, and pull out the items
	missing in the feed lookup tool. Then, try to get the series name for each
	unique series ID.
	'''
	exposed_process_new_fb(fetch_title)

def exposed_process_new_fb(fetch_title=False):
	'''
	Process items from Creative Novels/Fantasy-Books, and pull out the items
	missing in the feed lookup tool. Then, try to get the series name for each
	unique series ID.
	'''

	# This is probably broken for anyone else
	crn_feed_id = 589

	with db.session_context(override_timeout_ms=1000 * 60 * 15) as sess:

		print("Loading releases from database.")
		feed_q = sess.query(db.RssFeedPost)                                                           \
			.filter(db.RssFeedPost.published > datetime.datetime.now() - datetime.timedelta(days=30)) \
			.filter(db.RssFeedPost.feed_id == crn_feed_id)


		print("Generated query:", feed_q)
		feed_items = feed_q.all()

		print("Loaded %s items. Procesing." % (len(feed_items), ))
		items = proto_process_releases(sess, feed_items)

		print("Items:", len(items))
		out = []

		tags = {}
		for parsed, extracted in items["missed"]:
			if not extracted['tags']:
				print("No tags!")
				continue
			if len(extracted['tags']) != 1:
				print("What:", extracted)
				raise RuntimeError

			key = extracted['tags'][0]
			tags[key] = extracted

		for key, item in tags.items():
			sname, item_type = exposed_crn_series_type_from_chapter_url(item['linkUrl'])
			strtmp = "		('%s',                                                                   '%s',                                                                      '%s'), " % (
				key, sname, item_type)
			out.append(strtmp)




		print("Result")
		print()
		print("\n".join(out))

		# print("Missed: ", items["missed"])
