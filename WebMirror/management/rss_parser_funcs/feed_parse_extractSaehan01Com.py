def extractSaehan01Com(item):
	'''
	Parser for 'saehan01.com'
	'''


	badwords = [
			'Spanish translation',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		("Li Yu",                                     "In Love with an Idiot",                    'translated'),
		("Shameless",                                 "Shameless Gangster",                       'translated'),
		("Intoxication",                              "Intoxication",                             'translated'),
		("Lawless",                                   "Lawless Gangster",                         'translated'),
		("saye",                                      "SAYE",                                     'translated'),
		("Lawless Gangster",                          "Lawless Gangster",                         'translated'),
		("Advance Bravely",                           "Advance Bravely",                          'translated'),
		("addicted",                                  "Are you Addicted?",                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if "Lawless" in item['tags'] and "Gangster" in item['tags'] :
		return buildReleaseMessageWithType(item, "Lawless Gangster", vol, chp, frag=frag, postfix=postfix)
		
	return False