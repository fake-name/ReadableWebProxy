def extractUnluckyslimeWordpressCom(item):
	'''
	Parser for 'unluckyslime.wordpress.com'
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


	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, 'The Strange Adventure of a Broke Mercenary', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Broke Mercenary Chapter "):
		return buildReleaseMessageWithType(item, 'The Strange Adventure of a Broke Mercenary', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Hero of Black Chapter "):
		return buildReleaseMessageWithType(item, 'The Mightiest Hero of Black', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	return False