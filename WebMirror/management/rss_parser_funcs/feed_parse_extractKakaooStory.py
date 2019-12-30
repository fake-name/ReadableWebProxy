def extractKakaooStory(item):
	"""
	'Kakaoo Story'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('King of Hell’s Genius Pampered Wife Chapter'):
		return buildReleaseMessageWithType(item, 'King of Hell’s Genius Pampered Wife', vol, chp, frag=frag, postfix=postfix)
	return False
