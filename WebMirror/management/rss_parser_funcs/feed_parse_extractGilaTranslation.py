def extractGilaTranslation(item):
	"""
	# Gila Translation Monster

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	ltags = [tmp.lower() for tmp in item['tags']]
	if 'dawn traveler' in ltags and 'translation' in ltags:
		return buildReleaseMessageWithType(item, 'Dawn Traveler', vol, chp, frag=frag, postfix=postfix)
	if 'different world business symbol' in ltags and 'translation' in ltags:
		return buildReleaseMessageWithType(item, 'Different World Business Symbol', vol, chp, frag=frag, postfix=postfix)
	if 'star sea lord' in ltags and 'translation' in ltags:
		return buildReleaseMessageWithType(item, 'Star Sea Lord', vol, chp, frag=frag, postfix=postfix)
	if 'tensei shitara slime datta ken' in ltags and 'translation' in ltags:
		if not 'chapter' in item['title'].lower() and chp:
			frag = None
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	return False
