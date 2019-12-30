def extractFujitranslationWordpressCom(item):
	'''
	Parser for 'fujitranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('My Wife is a Martial Alliance Head',                 'My Wife is a Martial Alliance Head',               'translated'), 
		('My CEO Wife',                                        'My CEO Wife',                                      'translated'), 
		('Mai Kitsune Waifu',                                  'Mai Kitsune Waifu',                                'translated'), 
		('Rebirth of the Super Thief',                         'Rebirth of the Super Thief',                       'translated'), 
		('Matchless Supernatural of the Three Kingdom',        'Matchless Supernaturals of the Three Kingdom',     'translated'), 
		('Matchless Supernaturals of the Three Kingdom',       'Matchless Supernaturals of the Three Kingdom',     'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False