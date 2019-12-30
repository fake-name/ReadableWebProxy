def extractClicky(item):
	"""
	# Clicky Click Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'MEMORIZE' in item['tags']:
		return buildReleaseMessageWithType(item, 'MEMORIZE', vol, chp, frag=frag, postfix=postfix)
	if 'R8CM' in item['tags']:
		return buildReleaseMessageWithType(item, 'Revolution of the 8th Class Mage', vol, chp, frag=frag, postfix=postfix)
	if 'Dusk Howler' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dusk Howler', vol, chp, frag=frag, postfix=postfix)
	if 'Legendary Moonlight Sculptor' in item['tags'] and any([('Volume' in tag) for tag in item['tags']]):
		return buildReleaseMessageWithType(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)
	return False
