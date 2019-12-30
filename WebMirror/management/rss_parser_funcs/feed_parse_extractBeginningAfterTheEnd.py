def extractBeginningAfterTheEnd(item):
	"""

	"""
	if 'turtleme.me' in item['linkUrl']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'The Beginning After The End', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False