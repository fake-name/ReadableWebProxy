def extractReincarnationTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if "Reincarnated as a Dragon's Egg" in item['tags']:
		return buildReleaseMessageWithType(item, "Reincarnated as a dragon's egg ～Lets aim to be the strongest～", vol, chp, frag=frag, postfix=postfix)
	return False
