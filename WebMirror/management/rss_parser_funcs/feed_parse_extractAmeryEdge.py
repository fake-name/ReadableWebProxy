def extractAmeryEdge(item):
	"""
	# 'Amery Edge'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Articles' in item['tags'] or 'Guides' in item['tags']:
		return None
	if 'Your Highness, I Know My Wrong' in item['tags'] or 'Your Highness, I Know My Wrongs' in item['tags']:
		return buildReleaseMessageWithType(item, 'Your Highness, I Know My Wrong', vol, chp, frag=frag, postfix=postfix)
	if '108 Star Maidens of Destiny' in item['tags']:
		return buildReleaseMessageWithType(item, '108 Star Maidens of Destiny', vol, chp, frag=frag, postfix=postfix)
	if 'Zombie Girl, Where Are You?' in item['tags']:
		return buildReleaseMessageWithType(item, 'Zombie Girl, Where Are You?', vol, chp, frag=frag, postfix=postfix)
	if 'Ultimate Assassin System' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ultimate Assassin System', vol, chp, frag=frag, postfix=postfix)
	if 'Assassin Farmer' in item['tags']:
		return buildReleaseMessageWithType(item, 'Assassin Farmer', vol, chp, frag=frag, postfix=postfix)
	if 'I Am A Killer' in item['tags']:
		return buildReleaseMessageWithType(item, 'I Am A Killer', vol, chp, frag=frag, postfix=postfix)
	if '108 Maidens of Destiny' in item['tags']:
		return buildReleaseMessageWithType(item, '108 Maidens of Destiny', vol, chp, frag=frag, postfix=postfix)
	return False
