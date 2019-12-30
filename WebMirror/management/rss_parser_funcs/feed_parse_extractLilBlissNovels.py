def extractLilBlissNovels(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if ':' in item['title'] and 'Side Story' in item['title'] and not postfix:
		postfix = item['title'].split(':')[-1]
	if 'Wei Wei Yi Xiao Hen Qing Cheng' in item['tags']:
		return buildReleaseMessageWithType(item, 'Wei Wei Yi Xiao Hen Qing Cheng', vol, chp, frag=frag, postfix=postfix)
	if 'Memory Lost' in item['tags']:
		return buildReleaseMessageWithType(item, 'Memory Lost', vol, chp, frag=frag, postfix=postfix)
	return False
