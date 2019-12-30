def extractChocolatranslationsWordpressCom(item):
	'''
	Parser for 'chocolatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Entertainment Industry\'s Gourmet Food Service',       'Entertainment Industry\'s Gourmet Food Service',                      'translated'),
		('Rebirth of a CV Star',                                 'Rebirth of a CV Star',                                                'translated'),
		('Rebirth into an Interstellar Marriage',                'Rebirth into an Interstellar Marriage',                               'translated'),
		('RIAIM',                                                'Rebirth into an Interstellar Marriage',                               'translated'),
		('Still Saving The World Today',       'Still Saving The World Today',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False