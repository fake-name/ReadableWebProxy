
GLOBAL_BAD_URLS = [
			'/xmlrpc.php',
			'gprofiles.js',
			'netvibes.com',
			'accounts.google.com',
			'edit.yahoo.com',
			'add.my.yahoo.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'twitter.com',
			'facebook.com',
			'public-api.wordpress.com',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'delicious.com',
			'paypal.com',
			'digg.com',
			'topwebfiction.com',
			'/page/page/',
			'addtoany.com',
			'stumbleupon.com',
			'delicious.com',
			'/comments/feed/',
			'fbcdn-',
			'/wp-json/',
			'reddit.com',
			'/osd.xml',
			'/wp-login.php',
			'?openidserver=1',
			'newsgator.com',
			'technorati.com',
			'pixel.wp.com',
			'a.wikia-beacon.com',
			'b.scorecardresearch.com',
			'//mail.google.com',
			'javascript:void',
			'twitter.com/intent/',
			'www.pinterest.com/pin/',
			'www.wattpad.com/login?',
			'/embed?',

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
	]
