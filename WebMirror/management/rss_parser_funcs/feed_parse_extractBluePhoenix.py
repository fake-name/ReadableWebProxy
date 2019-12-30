def extractBluePhoenix(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Chapter') and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, 'Blue Phoenix', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('Blue Phoenix Chapter ') and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, 'Blue Phoenix', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('Overthrowing Fate Chapter ') and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, 'Overthrowing Fate', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
