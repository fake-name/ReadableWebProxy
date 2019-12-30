def extractWatermelons(item):
	"""
	# World of Watermelons

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	matches = re.search('\\bB(\\d+)C(\\d+)\\b', item['title'])
	if 'The Desolate Era' in item['tags'] and matches:
		vol, chp = matches.groups()
		postfix = ''
		if '–' in item['title']:
			postfix = item['title'].split('–', 1)[-1]
		return buildReleaseMessageWithType(item, 'Mang Huang Ji', vol, chp, frag=frag, postfix=postfix)
	return False
