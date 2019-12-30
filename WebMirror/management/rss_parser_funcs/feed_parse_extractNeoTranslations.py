def extractNeoTranslations(item):
	"""
	# Neo Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Man Picked up by the Gods'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'The Man Picked up by the Gods', vol, chp, frag=frag, postfix=postfix)
	if 'I came back but the world is still a fantasy' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)
	if 'Ashes and Kingdoms' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ashes and Kingdoms', vol, chp, frag=frag, postfix=postfix)
	if 'Goblin Kingdom' in item['tags']:
		return buildReleaseMessageWithType(item, 'Goblin no Oukoku', vol, chp, frag=frag, postfix=postfix)
	return False
