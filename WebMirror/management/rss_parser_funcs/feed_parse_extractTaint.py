def extractTaint(item):
	"""

	"""
	titletmp = item['title'] + ' '.join(item['tags'])
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titletmp)
	if not (chp or vol or frag) and not 'preview' in item['title']:
		return False
	if 'Chapter Release' in item['tags'] and 'Taint' in item['tags'] and 'Main Story' in item['tags']:
		return buildReleaseMessageWithType(item, 'Taint', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Chapter Release' in item['tags'] and 'Taint' in item['tags'] and 'Side Story' in item['tags']:
		postfix = 'Side Story'
		return buildReleaseMessageWithType(item, 'Taint', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		
	if 'Chapter Release' in item['tags'] and 'trials' in item['tags']:
		return buildReleaseMessageWithType(item, 'Trials', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		
	return False