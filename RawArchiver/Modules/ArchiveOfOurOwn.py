
import urllib.parse
import RawArchiver.ModuleBase

class ArchiveOfOurOwnRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "ArchiveOfOurOwnRawModule"

	target_urls = [
		"https://archiveofourown.org/",
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
			"/about",
			"/search",
			"/abuse_reports/",
			"/known_issues",
			"/diversity",
			"/tos",
			"/dmca",

			"/comments/",
			"/kudos",
			"#share",
			"#comments",

			".epub?",
			".pdf?",
			".mobi?",

			"/join-us/",
			"/chat/",
			'&format=pdf',
			'?format=pdf',
			'?replytocom=',
			"/forum/",
			"/forum",
			"/forums/",
			"/forums",
			"/games/",
			"/betareaders/",
			"/poetry/", # Really?
			'/bookmarks/new',

			"?show_comments=",
			"/comments",

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
