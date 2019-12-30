def extractUDonateWeTranslate(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'ATG' in item['tags'] or 'Against the Gods' in item['title'] and 'Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Against the Gods', vol, chp, frag=frag, postfix=postfix)
	return False
