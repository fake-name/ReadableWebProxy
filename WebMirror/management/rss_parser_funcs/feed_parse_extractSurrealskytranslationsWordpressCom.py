def extractSurrealskytranslationsWordpressCom(item):
	'''
	Parser for 'surrealskytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('what to do when i become a koi and fall into the male god’s bathtub',       'what to do when i become a koi and fall into the male god’s bathtub',                      'translated'),
		('wdbkfmgb',                                                                  'what to do when i become a koi and fall into the male god’s bathtub',                      'translated'),
		('superstar aspiration',        'superstar aspirations',                      'translated'),
		('superstar aspirations',       'superstar aspirations',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False