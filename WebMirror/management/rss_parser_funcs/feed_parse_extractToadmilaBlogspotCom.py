def extractToadmilaBlogspotCom(item):
	'''
	Parser for 'toadmila.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	
	if item['title'].startswith("Chapter ") and vol is None:
		return buildReleaseMessageWithType(item, 'Toadmila Wartly', 1, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("Book "):
		return buildReleaseMessageWithType(item, 'Toadmila Wartly', vol, chp, frag=frag, postfix=postfix)


	return False