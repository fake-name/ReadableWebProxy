def extractSoojikisProject(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Weakest Skeleton' in item['tags'] or 'Home page' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kurasu marugoto jingai tensei -Saijyaku no sukeruton ni natta ore-', vol, chp, frag=frag, postfix=postfix)
	if 'Reincarnated as a Villager' in item['tags']:
		return buildReleaseMessageWithType(item, 'Reincarnated as a Villager ~ Strongest Slow-life', vol, chp, frag=frag, postfix=postfix)
	if 'Yandere?' in item['tags'] and 'Weapons' in item['tags']:
		return buildReleaseMessageWithType(item, 'Myself, weapons, and Yandere', vol, chp, frag=frag, postfix=postfix)
	return False
