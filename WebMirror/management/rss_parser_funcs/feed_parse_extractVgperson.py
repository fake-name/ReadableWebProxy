def extractVgperson(item):
	"""
	Parser for 'VgPerson'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'the Manga' in item['title']:
		return None
	
	if 'Vocaloid' in item['tags']:
		return None
	if 'twitter' in item['tags']:
		return None
		
	if 'WATTT' in item['tags']:
		return buildReleaseMessageWithType(item, 'WATTT', vol, chp, frag=frag, postfix=postfix)
	return False