def extractShinzoutlWordpressCom(item):
	'''
	Parser for 'shinzoutl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "I Bought a Girl" in item['tags']:
		return buildReleaseMessageWithType(item, "I Bought a Girl", vol, chp, frag=frag, postfix=postfix)

	if "Kisei Kanojo Sana" in item['tags']:
		return buildReleaseMessageWithType(item, "Kisei Kanojo Sana", vol, chp, frag=frag, postfix=postfix)

	return False