def extractItsametranslationWordpressCom(item):
	'''
	Parser for 'itsametranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('person with an inferior ability',       'person with inferior ability returns from demon world',                      'translated'),
		('person with inferior ability returns from demon world',       'person with inferior ability returns from demon world',                      'translated'),
		('another world is full of happiness',       'another world is full of happiness',                      'translated'),
		('the iceblade magician rules over the world',       'the iceblade magician rules over the world',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False