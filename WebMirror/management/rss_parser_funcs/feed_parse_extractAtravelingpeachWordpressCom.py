def extractAtravelingpeachWordpressCom(item):
	'''
	Parser for 'atravelingpeach.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['title'].startswith("Chapter ") and item['tags'] == ['Uncategorized']:
			return buildReleaseMessageWithType(item, 'After the Cannon Fodder’s Rebirth', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False