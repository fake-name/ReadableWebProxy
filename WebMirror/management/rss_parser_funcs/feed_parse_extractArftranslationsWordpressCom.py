def extractArftranslationsWordpressCom(item):
	'''
	Parser for 'arftranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "The Support Manages the Adventurer Parties!!", vol, chp, frag=frag, postfix=postfix)
		

	return False