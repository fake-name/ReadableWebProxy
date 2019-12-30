def extractLingson(item):
	"""
	# Lingson's Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Legendary Thief' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessageWithType(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)
	if 'ALBT Chapter Release' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessageWithType(item, 'Assassin Landlord Beauty Tenants', vol, chp, frag=frag, postfix=postfix)
	return False
