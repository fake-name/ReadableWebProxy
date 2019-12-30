def extractNotsofriendlytranslationsWordpressCom(item):
	'''
	Parser for 'notsofriendlytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			("Venom Tongue – c",          "I Quit the Going-Home Club for a Girl with a Venomous Tongue",                                                   "Translated"),
			("Villainess’ Father – c",    "Since I’ve Reincarnated as the Villainess’ Father, I’ll Shower My Wife and Daughter in Love",                    "Translated"),
			("Villainess Father – c",     "Since I’ve Reincarnated as the Villainess’ Father, I’ll Shower My Wife and Daughter in Love",                    "Translated"),
			("Kage Ga Usui –c",           "Hazure Skill “Kage ga Usui” o Motsu Guild Shokuin ga, Jitsuha Densetsu no Ansatsusha",                    "Translated"),
			("Kage Ga Usui – c",          "Hazure Skill “Kage ga Usui” o Motsu Guild Shokuin ga, Jitsuha Densetsu no Ansatsusha",                    "Translated"),
			("Aristocrat Assassin – c",   "The Best Assassin, Incarnated into a Different World’s Aristocrat",                                                     "Translated"),
			# ("",                          "Mysetious Job Oda Nobunguna",                                             "Translated"),
			# ("",                          "It Seems like My Body Is Completely Invincible",                          "Translated"),
			# ("",                          "The Hero Who Returned Remains the Strongest in the Modern World",         "Translated"),
			# ("",                          "Isekai cheat Magician",                                                   "Translated"),
		]         

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False