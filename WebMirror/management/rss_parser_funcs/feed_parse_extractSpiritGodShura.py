def extractSpiritGodShura(item):
	"""
	# Sousetsuka
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Chapter') and item['tags'] == ['Chapters']:
		if ':' in item['title'] and not postfix:
			postfix = item['title'].split(':')[-1]
		return buildReleaseMessageWithType(item, 'Spirit God Shura', vol, chp, postfix=postfix, tl_type='oel')
	return False
