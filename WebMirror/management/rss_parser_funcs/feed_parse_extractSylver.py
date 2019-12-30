def extractSylver(item):
	"""
	# Sylver Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if "History's Number One Founder" in item['tags']:
		if ':' in item['title']:
			postfix = item['title'].split(':', 1)[-1].strip()
		return buildReleaseMessageWithType(item, "History's Number One Founder", vol, chp, frag=frag, postfix=postfix)
	if 'The Gate of Extinction' in item['tags']:
		if ':' in item['title']:
			postfix = item['title'].split(':', 1)[-1].strip()
		return buildReleaseMessageWithType(item, 'The Gate of Extinction', vol, chp, frag=frag, postfix=postfix)
	if "Shura's Wrath" in item['tags'] or 'Shura"s Wrath' in item['tags']:
		if ':' in item['title']:
			postfix = item['title'].split(':', 1)[-1].strip()
		return buildReleaseMessageWithType(item, "Shura's Wrath", vol, chp, frag=frag, postfix=postfix)
	return False
