def extractBiusyublushWordpressCom(item):
	'''
	Parser for 'biusyublush.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Under the Power',                  'Under The Power – Lan Se Shi',                      'translated'),
		('under the power [锦衣之下]',       'Under The Power – Lan Se Shi',                      'translated'),
		('锦衣之下',                         'Under The Power – Lan Se Shi',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False