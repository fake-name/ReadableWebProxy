def extractThrowaway(item):
	"""
	Parser for 'Throwaway'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if item['title'].lower().startswith('sisters violated many times in dreams and reality') or \
		item['title'].lower().startswith('sisters violated many times in dream and reality'):
		return buildReleaseMessageWithType(item, 'Sisters Violated Many Times in Dreams and Reality', vol, chp, frag=frag, postfix=postfix)
	
	if 'WATTT' in item['tags']:
		return buildReleaseMessageWithType(item, 'WATTT', vol, chp, frag=frag, postfix=postfix)
		
	return False