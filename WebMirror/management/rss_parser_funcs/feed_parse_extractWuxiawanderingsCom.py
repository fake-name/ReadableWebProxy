def extractWuxiawanderingsCom(item):
	'''
	Parser for 'wuxiawanderings.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('jade tiger',       'The Jade Tiger',                      'translated'),
		('rain of blood',    'A Rain of Blood Stains Flowers Red',  'translated'),
		('PRC',              'PRC',                                 'translated'),
		('Loiterous',        'Loiterous',                           'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False