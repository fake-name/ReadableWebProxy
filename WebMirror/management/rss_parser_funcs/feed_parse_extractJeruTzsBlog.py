def extractJeruTzsBlog(item):
	"""
	JeruTz's Blog
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Vandread' in item['tags'] and 'Extra Stage' in item['tags']:
		return buildReleaseMessageWithType(item, "VANDREAD the Extra Stage", vol, chp, frag=frag, postfix=postfix)
		
		
	return False