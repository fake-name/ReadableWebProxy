def extractXianXiaWorld(item):
	"""
	Xian Xia World
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'www.xianxiaworld.net/A-Thought-Through-Eternity/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'A Thought Through Eternity', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Beast-Piercing-The-Heavens/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'Beast Piercing The Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Dominating-Sword-Immortal/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'Dominating Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Dragon-Marked-War-God/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'Dragon-Marked War God', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Emperor-of-The-Cosmos/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'Emperor of The Cosmos', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/God-of-Slaughter/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'God of Slaughter', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/God-level-Bodyguard-in-The-City/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'God-level Bodyguard in The City', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Realms-In-The-Firmament/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'Realms In The Firmament', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/The-King-Of-Myriad-Domains/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'The King Of Myriad Domains', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/The-Magus-Era/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'The Magus Era', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/The-Portal-of-Wonderland/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'The Portal of Wonderland', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/World-Defying-Dan-God/' in item['linkUrl']:
		return buildReleaseMessageWithType(item, 'World Defying Dan God', vol, chp, frag=frag, postfix=postfix)
	return False
