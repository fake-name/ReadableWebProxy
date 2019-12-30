def extractKaezar(item):
	"""
	# Kaezar Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Mushoku Tensei' in item['tags'] and (chp or vol):
		if 'Redundancy Chapters' in item['tags']:
			return buildReleaseMessageWithType(item, 'Mushoku Tensei Redundancy', vol, chp, frag=frag, postfix=postfix)
		else:
			return buildReleaseMessageWithType(item, 'Mushoku Tensei', vol, chp, frag=frag, postfix=postfix)
	return False
