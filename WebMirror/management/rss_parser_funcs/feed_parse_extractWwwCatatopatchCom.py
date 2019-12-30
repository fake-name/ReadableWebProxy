def extractWwwCatatopatchCom(item):
	'''
	Parser for 'www.catatopatch.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('The Devil\'s Evolution Catalog ',  'The Devil\'s Evolution Catalog',      'translated'),
		('The Undying Drama',                'The Undying Drama',                   'translated'),
		('Marquis of Grand Xia',             'Marquis of Grand Xia',                'translated'),
		('Appraiser\'s Job',                 'Appraiser\'s Job',                    'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False