def extractOmgitsaray(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('9HTM',               '9 Heavenly Thunder Manual',                                  'translated'),
		('undefeatable',       'Leveling Up And Becoming Undefeatable',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if 'chapter' in item['title'].lower() and (item['tags'] == ['Uncategorized', 'xianxia'] or item['tags'] == ['Uncategorized']):
		return buildReleaseMessageWithType(item, '9 Heavenly Thunder Manual', vol, chp, frag=frag, postfix=postfix)
		
		
	return False