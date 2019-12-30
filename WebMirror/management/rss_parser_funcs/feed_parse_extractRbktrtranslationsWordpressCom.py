def extractRbktrtranslationsWordpressCom(item):
	'''
	Parser for 'rbktrtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Residence of Monsters',              'Residence of Monsters',                             'translated'),
		('Jin Xiao Yi Tan',                    'Jin Xiao Yi Tan',                                   'translated'),
		('I Think My Boyfriend Is Sick',       'I Think My Boyfriend Is Sick',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False