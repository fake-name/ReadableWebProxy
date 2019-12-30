def extractTrashmtlWordpressCom(item):
	'''
	Parser for 'trashmtl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Dungeon Game',                    'Dungeon Game',                                   'translated'),
		('Nee-chan is a Soap Girl!?',       'Nee-chan is a Soap Girl!?',                      'translated'),
		('Prisoner of the Library',         'Prisoner of the Library',                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False