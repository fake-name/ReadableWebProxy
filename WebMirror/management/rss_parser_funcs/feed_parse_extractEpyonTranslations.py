def extractEpyonTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'magic robot aluminare ch' in item['title'].lower():
		match = re.search('ch ?(\\d+)\\-(\\d+)', item['title'])
		if match:
			chp = match.group(1)
			frag = match.group(2)
			return buildReleaseMessageWithType(item, 'Magic Robot Aluminare', vol, chp, frag=frag, postfix=postfix)
		return buildReleaseMessageWithType(item, 'Magic Robot Aluminare', vol, chp, frag=frag, postfix=postfix)
	return False
