def extractGirlyNovels(item):
	"""
	Girly Novels
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'The Captivating Crown Prince' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Captivating Crown Prince', vol, chp, frag=frag, postfix=postfix)
	if 'chongfei manual' in item['tags']:
		return buildReleaseMessageWithType(item, 'Chongfei Manual', vol, chp, frag=frag, postfix=postfix)
	if 'Black Belly Wife' in item['tags']:
		return buildReleaseMessageWithType(item, 'Black Belly Wife', vol, chp, frag=frag, postfix=postfix)
	if 'The Royals Cute Little Wife' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Royals Cute Little Wife', vol, chp, frag=frag, postfix=postfix)
	if 'Prince' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Captivating Crown Prince', vol, chp, frag=frag, postfix=postfix)
	if 'empress' in item['tags']:
		return buildReleaseMessageWithType(item, 'Beloved Empress', vol, chp, frag=frag, postfix=postfix)
		
	return False