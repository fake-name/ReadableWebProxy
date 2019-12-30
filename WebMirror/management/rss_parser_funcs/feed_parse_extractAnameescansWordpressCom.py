def extractAnameescansWordpressCom(item):
	'''
	Parser for 'anameescans.wordpress.com'
	'''

	if 'Manhua' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Contract Marriage',         'Contract Marriage',                        'translated'),
		('Nowhere to be Found',       'Nowhere to be Found',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False