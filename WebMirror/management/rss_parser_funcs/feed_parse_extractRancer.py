def extractRancer(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Strongest Magical Beast' in item['tags'] and 'Chapter Release' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'The Strongest Magical Beast', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Apocalypse ЯR' in item['tags'] and 'Chapter Release' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Apocalypse ЯR', vol, chp, frag=frag, postfix=postfix)
	if 'Legend of Xing Feng' in item['tags']:
		return buildReleaseMessageWithType(item, 'Legend of Xingfeng', vol, chp, frag=frag, postfix=postfix)
	if 'The Exceptional Godly Thief-The Good for Nothing Seventh Young Lady' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Good for Nothing Seventh Young Lady', vol, chp, frag=frag, postfix=postfix)
	return False
