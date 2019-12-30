def extractEgscansCom(item):
	'''
	Parser for 'egscans.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if 'Manga' in item['tags']:
		return None
	if 'Manhua' in item['tags']:
		return None
	if 'Manhwa (Korean)' in item['tags']:
		return None
	if 'webtoon (webcomic)' in item['tags']:
		return None
	if 'Manga (Japanese)' in item['tags']:
		return None

	if "WATTT" in item['tags']:
		return buildReleaseMessageWithType(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False