def extractNatsuTl(item):
	"""
	# Natsu TL
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Jikuu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Jikuu Mahou de Isekai to Chikyuu wo ittarikitari', vol, chp, frag=frag, postfix=postfix)
	if 'Magi Craft Meister' in item['tags']:
		return buildReleaseMessageWithType(item, 'Magi Craft Meister', vol, chp, frag=frag, postfix=postfix)
	return False
