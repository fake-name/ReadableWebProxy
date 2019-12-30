def extractChronaZero(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'tensei jinsei' in item['tags']:
		return buildReleaseMessageWithType(item, 'Cheat Aru Kedo Mattari Kurashitai《Tensei Jinsei o Tanoshimou!》', vol, chp, frag=frag, postfix=postfix)
	if 'Level up by walking' in item['tags']:
		return buildReleaseMessageWithType(item, 'Level up By Walking: in 10 thousand steps I will be level 10000', vol, chp, frag=frag, postfix=postfix)
	if 'When you actually went to be another world not as the Hero but as the Slave and then...' in item['tags']:
		return buildReleaseMessageWithType(item, 'When you actually went to be another world not as the Hero but as the Slave and then...', vol, chp, frag=frag, postfix=postfix)
	return False
