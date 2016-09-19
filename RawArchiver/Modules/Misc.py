
import urllib.parse
import RawArchiver.ModuleBase

class WebComicsRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "MiscRawModule"

	target_urls = [
		'http://www.scp-wiki.net/',
		'http://scp-wiki.net/',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
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

		"/blog/",
		"/forums/",

	 # Block loaded resources
		"project/load.php",

	 # Yes, I only speak&read english. Leave me to my filtering shame.
		"Category:Brazilian",
		"Category:Brazilian_Portuguese",
		"Category:Czech",
		"Category:Bulgarian",
		"Category:Esperanto",
		"Category:Filipino",
		"Category:French",
		"Category:German",
		"Category:Greek",
		"Category:Hungarian",
		"Category:Indonesian",
		"Category:Italian",
		"Category:Korean",
		"Category:Lithuanian",
		"Category:Norwegian",
		"Category:Polish",
		"Category:Romanian",
		"Category:Russian",
		"Category:Spanish",
		"Category:Turkish",
		"Category:Vietnamese",
		"Special:RecentChangesLinked",
		"Format_guideline",
		"(Bahasa_Indonesia)",

		"(Indonesia)",
		"(German)",
		"(French)",
		"(Russian)",
		"(Italian)",
		"(Romanian)",
		"(Norwegian)",
		"(Lithuanian)",
		"(Greek)",
		"~Brazilian_Portuguese~",
		"(Filipino)",
		"(Esperanto)",
		"(Spanish)",
		"(Vietnamese)",
		"(Brazilian_Portuguese)",
		"(Polish)",
		"(Hungarian)",
		"(Korean)",
		"(Turkish)",
		"(Czech)",

	 # misc
		"viewforum.php",
		"viewtopic.php",
		"memberlist.php",
		"printable=yes",
		"/forums/",
		"title=Special",
		"action=edit",
		"action=history",
		"action=info",
		"title=Help:",
		"title=User_talk:",
		"&oldid=",
		"oldid=",
		"title=Special:Book",

		"Special:WhatLinksHere",
		"Special:UserLogin",
		"Special:",
		"action=edit",
		"diff=",
		"oldid=",
		"diff%3D",
		"oldid%3D",
		"feed=atom",
		"action=submit",

		"~Russian_Version~",
		"~Russian",
		"~Brazilian",

	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]
