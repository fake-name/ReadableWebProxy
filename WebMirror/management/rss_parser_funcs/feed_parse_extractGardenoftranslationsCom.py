def extractGardenoftranslationsCom(item):
	'''
	Parser for 'gardenoftranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Books to Dominate Married Women',       'Books to Dominate Married Women',                      'translated'),
		('Isekai tensei no boukensha',            'Isekai tensei no boukensha',                           'translated'),
		('Destination of Crybird',                'Destination of Crybird',                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False