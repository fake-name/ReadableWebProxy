
GLOBAL_BAD_URLS = [
			'//mail.google.com',
			'/comments/feed/',
			'/embed?',
			'/osd.xml',
			'/page/page/',
			'/wp-json/',
			'/wp-login.php',
			'/xmlrpc.php',
			'?openidserver=1',
			'a.wikia-beacon.com',
			'accounts.google.com',
			'add.my.yahoo.com',
			'addtoany.com',
			'b.scorecardresearch.com',
			'delicious.com',
			'digg.com',
			'edit.yahoo.com',
			'facebook.com',
			'fbcdn-',
			'feeds.wordpress.com',
			'gprofiles.js',
			'javascript:void',
			'netvibes.com',
			'newsgator.com',
			'paypal.com',
			'pixel.wp.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'reddit.com',
			'stumbleupon.com',
			'technorati.com',
			'topwebfiction.com',
			'twitter.com',
			'twitter.com/intent/',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'www.addtoany.com'
			'www.pinterest.com/pin/',
			'www.wattpad.com/login?',

			'www.paypalobjects.com',

			# Tumblr can seriously go fuck itself with a rusty stake
			'tumblr.com/widgets/',
			'www.tumblr.com/login',
			'://tumblr.com',
			'&share=tumblr',

			'/wp-content/plugins/',
			'/wp-content/themes/',
			'/wp-json/oembed/',

			# At least one site (booksie) is serving the favicon with a mime-type
			# of "text/plain", which then confuses the absolute crap out of the
			# mime-type dispatcher.
			# Since I'm not re-serving favicons anyways, just do not fetch them ever.
			'favicon.ico',

			# Try to not scrape inline images
			';base64,',

			"www.fashionmodeldirectory.com",
			"www.watchingprivatepractice.com",
			"Ebonyimages.jupiterimages.com",

			# More garbage issues.
			'"https',
			'#comment-',
			'/oembed/1.0/',
			'&share=',
			'replytocom=',
			'?feed=rss2&page_id',
			'?share=tumblr',
			'?share=facebook',

			'chasingadreamtranslations.com/?fp=',

			# NFI where /this/ came from
			'www.miforcampuspolice.com',
			'tracking.feedpress.it',

			'www.quantcast.com',

			'mailto:',
			'javascript:popupWindow(',

			'en.blog.wordpress.com',

			'counter.yadro.ru',


			'/js/js/',
			'/css/css/',
			'/images/images/',
			'ref=dp_brlad_entry',
			'https:/www.',
	]


GLOBAL_DECOMPOSE_BEFORE = [
			{'name'     : 'likes-master'},  # Bullshit sharing widgets
			{'id'       : 'jp-post-flair'},
			{'class'    : 'post-share-buttons'},
			{'class'    : 'commentlist'},  # Scrub out the comments so we don't try to fetch links from them
			{'class'    : 'comments'},
			{'id'       : 'comments'},
		]

GLOBAL_DECOMPOSE_AFTER = []


RSS_SKIP_FILTER = [
	"www.baka-tsuki.org",
	"re-monster.wikia.com",
	'inmydaydreams.com',
	'www.fanfiction.net',
	'www.booksie.com',
	'www.booksiesilk.com',
	'www.fictionpress.com',
	'storiesonline.net',
	'www.fictionmania.tv',
	'pokegirls.org',
	'www.asstr.org',
	'www.mcstories.com',
	'www.novelupdates.com',
	'40pics.com',
	'#comment-',

]


RSS_TITLE_FILTER = [
	"by: ",
	"comments on: ",
	"comment on: ",
	"comment on ",
]


# Goooooo FUCK YOURSELF
GLOBAL_INLINE_BULLSHIT = [

			"This translation is property of Infinite Novel Translations.",
			"This translation is property of Infinite NovelTranslations.",
			"If you read this anywhere but at Infinite Novel Translations, you are reading a stolen translation.",
			"&lt;Blank&gt;",
			"&lt;space&gt;",
			"<Blank>",
			"<Blank>",
			"please read only translator’s websitewww.novitranslation.com",
			"please read only translator’s website www.novitranslation.com",
			"Please do not host elsewhere but MBC and Yumeabyss",
			'Original and most updated translations are from volaretranslations.',
			'Please support the translator for Wild Consort by reading on volarenovels!',
			'Original and most updated translations are from volaretranslations.',
			'Original and most updated translations are from volaretranslations.',
			"&lt;StarveCleric&gt;",
			'(trytranslations.com at your service!)',
			'Please do not host elsewhere but volare and Yumeabyss',

]
