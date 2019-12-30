def extractCloudyTranslations(item):
	'''
	Parser for 'Cloudy Translations'
	'''
	
	if 'wedding' in item['tags']:
		# Really?
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		("Kill The Dragon",                                                               "Kill The Dragon",                                                                  'translated'),
		("The Reborn Little Girl Won't Give Up",                                          "The Reborn Little Girl Won't Give Up",                                             'translated'),
		("KonjikinoWordMasster",                                                          "Konjiki no Word Master (LN)",                                                      'translated'),
		("The Saint's Magic Power is Omnipotent",                                         "The Saint's Magic Power is Omnipotent (LN)",                                       'translated'),
		("Regarding the Duke with Gynophobia and the Eccentric Lady Scholar",             "Regarding the Duke with Gynophobia and the Eccentric Lady Scholar",                'translated'),
		("The White Cat that Swore Vengeance was Just Lazying on the Dragon King’s Lap",  "The White Cat that Swore Vengeance was Just Lazying on the Dragon King’s Lap",     'translated'),
		("Regarding the Duke with Gynophobia and the Eccentric Lady Scholar",             "Regarding the Duke with Gynophobia and the Eccentric Lady Scholar",                'translated'),
		("aku no joou no kiseki",                                                         "Aku no Joou no Kiseki",                                                            'translated'),
		("The Beauty's Secret",                                                           "The Beauty's Secret",                                                              'translated'),
		("shut-in magician",                                                              "Shut-in Magician",                                                                 'translated'),
		("I Quit Being a Noble and Became a Commoner",                                    "I Quit Being a Noble and Became a Commoner",                                       'translated'),
		("Drop!!　～A Tale of the Fragrance Princess～",                                  "Drop!! ~A Tale of the Fragrance Princess~ [LN]",                                   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False