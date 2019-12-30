def extractDemonScorpionTranslations(item):
	"""
	Demon Scorpion Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'MER' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial Emperor Reborn', vol, chp, frag=frag, postfix=postfix)
	if 'Arcane D' in item['tags']:
		return buildReleaseMessageWithType(item, 'Arcane Devastation', vol, chp, frag=frag, postfix=postfix)
		
	return False