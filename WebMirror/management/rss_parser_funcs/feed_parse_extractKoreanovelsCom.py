def extractKoreanovelsCom(item):
	'''
	Parser for 'koreanovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['title'].startswith("Link ") and item['tags'] == ['RSS']:
		return buildReleaseMessageWithType(item, 'Level 1 Skeleton', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	if item['title'].startswith("MoS Link ") and item['tags'] == ['RSS']:
		return buildReleaseMessageWithType(item, 'Master of Strength', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False