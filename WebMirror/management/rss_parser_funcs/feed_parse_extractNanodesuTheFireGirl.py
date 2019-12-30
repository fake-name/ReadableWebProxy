def extractNanodesuTheFireGirl(item):
	"""
	Parser for '(NanoDesu) - The Fire Girl'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if "Complete" in item['title'] and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, 'Fire Girl', vol, chp, frag=frag, postfix=postfix)
	return False