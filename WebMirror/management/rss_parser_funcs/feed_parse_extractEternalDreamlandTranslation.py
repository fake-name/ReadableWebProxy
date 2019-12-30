def extractEternalDreamlandTranslation(item):
	"""
	Eternal Dreamland Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Amorous Slave Girl' in item['tags']:
		return buildReleaseMessageWithType(item, 'Amorous Slave Girl', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Blood Warrior' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Blood Warrior', vol, chp, frag=frag, postfix=postfix)
	if 'Love Affair With Sister-In-Law' in item['tags']:
		return buildReleaseMessageWithType(item, 'Love Affair With Sister-In-Law', vol, chp, frag=frag, postfix=postfix)
	if 'Peerless Demonic Lord' in item['tags']:
		return buildReleaseMessageWithType(item, 'Peerless Demonic Lord', vol, chp, frag=frag, postfix=postfix)
	return False
