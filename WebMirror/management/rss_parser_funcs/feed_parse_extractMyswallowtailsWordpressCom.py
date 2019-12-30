def extractMyswallowtailsWordpressCom(item):
	'''
	Parser for 'myswallowtails.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Rebirth of High Female Entropy',       'Rebirth of High Female Entropy',                                         'translated'),
		('rebirth',                              'Rebirth of High Female Entropy',                                         'translated'),
		('Frosty Prince',                        'Frosty Prince Boils Over his Imperial Concubine:Generals Di Daughter',   'translated'),
	]


	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False