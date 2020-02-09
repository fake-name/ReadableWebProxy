
import urllib.parse
import RawArchiver.ModuleBase

class WebComicsRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "WebComicsRawModule"

	# TODO: Support cloudfront resources
	target_urls = [
		'http://cfw.me',
		'http://comicfury.com',
		'http://the-comic.org',
		'http://thecomicseries.com',
		'http://thecomicstrip.org',
		'http://webcomic.ws',
		'http://webcomic.ws',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
		'/characters/characters/',
		'/comic/chap4/comic/',
		'/comic/chap4/donator/',
		'/comic/chap4/images/comic/chapters/',
		'&destination=blog%',
		'&destination=archive%',
		'search.php',
		"&replytocom=",
		"/viewtopic.php",
		'/viewforum.php',
		'/forum/index.php',
		"www.smbc-comics.com/smbcforum/",
		'destination=node',
		'rest_route=',
		'ucp.php',
		'mode=resend_act',
		'/archive/comments',
		'title=&field_comic_number_value',
		'%2Flist%3Forder%3Dcreated%26sort%3Dasc%26page%3D2%26date_filter%5Bmax',
		'title%3D%26field_comic_number_value%3D',
		'%3Fpage%3D20%26permalink%',
		'destination=taxonomy',
		'wasted-talent-newsletter',
		'/topic/misc',
		'permalink',
		'/shop/product/comic-print',
		'replytocom=',
		'wastedtalentca-website&q=forum/wastedtalentca-website&q=forum',
		'site-upgrade.html/feed.xml',
		'.html/feed',
		'&_debug=',
		'/help/styles/default/xenforo/',
		r'\'!>\n',
		'share=google-plus-',

		'/topic/news&q=blog/',
		'/topic/engineering&q=comic/topic/engineering&q=comic/',
		'/it-never-ends&q=comic/it-never-ends&q=comic/',
		"/happy-day?q=comic/happy-day&q=comic/",
		'/fun-everyone&q=comic/fun-everyone&q=comic/',
		'/incommuni-coiffure&q=comic/incommuni-coiffure&q=comic/',
		'/ikea-dilemma&q=comic/ikea-dilemma&q=comic/',
		'/webcomics&q=category/web-links/',
		'/lost-omens&q=forum/lost-omens&q=forum/',
		'/mergency-supply&q=comic/mergency-supply&q=comic/',

		'/jam/book-one-we-are-engineers&q=blog/jam/',
		'www.wastedtalent.ca/forum/',
		'/red?q=character/red&q=character/',
		'/topic/vancouver&q=comic/topic/',
		'/ferry-times?q=comic/ferry-times&q=comic/',
		'/office-life?q=tags/office-life&q=tags/',
		'/general&q=forum/general&q=forum/',

		'/time-traveler&q=comic/time-traveler&q=comic/',
		'/christmas-wishes&q=comic/christmas-wishes&q=comic/',
		'/time-traveler&q=comic/time-traveler&q=comic/',

		'/preventative-measures&q=comic/preventative-measures&q=comic/',
		'/topic/ubc&q=comic/topic/',
		'/topic/games&q=comic/topic/',
		'/preventative-measures&q=comic/preventative-measures&q=comic/',
		'&_debug=1&_debug=1&_debug=1&',
		'/news&q=blog/topic/news&q=blog/',
		'/ftw&q=comic/ftw&q=comic/',
		'/hey-good-lookin&q=comic/hey-good-lookin&q=comic/',
		'/styling-secrets&q=comic/styling-secrets&q=comic/',
		'/technically-speaking&q=comic/technically-speaking&q=comic/',
		'/lost-omens&q=forum/lost-omens&q=forum/',
		'/topic/news&q=blog/topic/',
		'/ftw&q=comic/ftw&q=comic/',
		'/hey-good-lookin&q=comic/hey-good-lookin&q=comic/',
		'/styling-secrets&q=comic/styling-secrets&q=comic/',
		'/technically-speaking&q=comic/technically-speaking&q=comic/',
		'/games&q=comic/topic/games&q=comic/topic/',
		'/general&q=forum/general&q=forum/',
		'/lost-omens&q=forum/lost-omens&q=forum/',
		'/news?q=blog/topic/news&q=blog/',
		'/jam&q=character/jam&q=character/',
		'www.wastedtalent.ca/forum/',
		'/lucky?q=character/lucky&q=character/',
		'/red?q=character/red&q=character/',
		'/trevor?q=character/trevor&q=character/',
		'/dystopian-fashionista?q=comic/dystopian-fashionista&q=comic/',
		'/topic/art?q=comic/topic/art&q=comic/',
		'/length-matters&q=comic/length-matters&q=comic/',
		'/topic/engineering?q=comic/topic/engineering&q=comic/',
		'/topic/vancouver?q=comic/topic/vancouver&q=comic/',
		'/general?q=forum/general&q=forum/general&q=forum/',
		'/lost-omens?q=forum/lost-omens&q=forum/',
		'/office-life?q=tags/office-life&q=tags/',
		'/handbasketd&q=comic/handbasketd&q=comic/',
		'/stop-asking&q=comic/stop-asking&q=comic/',
		'www.comedity.com/ColorMe/v2.0/images/www.comedity.com/',
		'/printthread.php?',
		'/forums/newreply.php',
		'?do=newreply&',
		'/forums/showsinglepost.php',
		'&_debug=1&_debug=1&',
		'www.giantitp.com/forums/',
		'www.giantitp.com/cgi-bin/',
		'www.finderskeepers.gcgstudios.com/blog/',
		'/comic/chap6/story/images/comic/',
		'?p=comic&',
		'/comic/chap6/story/donator/',
		'/story/donator/',
		'/comic/chap1/characters/images/',
		'/comic/chap1/characters/world/',
		'/comic/chap1/images/comic/',
		'/comic/chap3/images/comic/',
		'/comic/chap3/images/story/',
		'/comic/chap4/images/comic/',
		'/comic/chap5/comic/chap5/',
		'/comic/chap5/images/comic/',
		'/comic/chap6/comic/chap3/',
		'/comic/chap6/images/comic/',
		'/comic/chap6/images/donator/',
		'/comic/chap6/mrc/characters/',
		'/comic/chap6/mrc/comic/',
		'/comic/chap6/mrc/images/',
		'/comic/chap6/mrc/mrc/',
		'/comic/chap6/mrc/world/',
		'/comic/chap6/story/images/',
		'/comic/chap3/images/mrc/',
		'www.userfriendly.org/cgi-bin/',
		'www.gpf-comics.com/wikix/',
		'index.php/Special:',
		'/index.php/fan-gallery/',
		'/index.php/themes/',
		'/vlozress/css/',
		'/wordpress/themes/',
		'/index.php/wordpress/',
		'/themes/vlozress/',
		'/js/themes/',
		'/sharenAlliance/css/',
		'/themes/sharenAlliance/',
		'/common/js/',
		'/js/wordpress/',
		'/wiki/themes/',



		# Fucking forumns ruin everything.
		'.keenspot.com/forum/',
		'www.comedity.com/forums/',
		'www.samandfuzzy.com/forum/',
		'www.comedity.com/www.comedity.com/',
	]

	bad_segments = [
		'announcements',
		'common',
		'css',
		'drowforums',
		'fan-gallery',
		'images',
		'index.php',
		'js',
		'sharenAlliance',
		'themes',
		'vlozress',
		'wiki',
		'wordpress',
	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False

		nl = urllib.parse.urlparse(url).netloc

		return any([nl.endswith(tgt) for tgt in cls.target_tlds])

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]
