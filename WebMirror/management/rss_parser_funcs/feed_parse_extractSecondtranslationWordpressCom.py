def extractSecondtranslationWordpressCom(item):
	'''
	Parser for 'secondtranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Uncategorized'] and (item['title'].startswith("Chapter ") or item['title'].startswith("Volume ") or item['title'].startswith("V2 ")):
		return buildReleaseMessageWithType(item, 'The Old Man Who Got a Second Round in Another World', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
		

	return False