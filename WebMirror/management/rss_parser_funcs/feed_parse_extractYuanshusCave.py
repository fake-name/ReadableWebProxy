def extractYuanshusCave(item):
	"""
	"Yuanshu's Cave"
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'id' in item['tags']:
		return buildReleaseMessageWithType(item, 'Id Fusion Story & Fantasy', vol, chp, frag=frag, postfix=postfix)
	if 'President Wife Is A Man' in item['tags']:
		return buildReleaseMessageWithType(item, 'President Wife is A Man', vol, chp, frag=frag, postfix=postfix)
	if 'Feng Yu Jiu Tian' in item['tags']:
		return buildReleaseMessageWithType(item, 'Feng Yu Jiu Tian', vol, chp, frag=frag, postfix=postfix)
	return False