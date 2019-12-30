def extractNorvaBlog(item):
	"""
	'Norva Blog'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Episode "):
		return buildReleaseMessageWithType(item, 'Sairin Yuusha no Fukushuu Hanashi', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	return False