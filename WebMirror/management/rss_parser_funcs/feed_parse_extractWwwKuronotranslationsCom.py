def extractWwwKuronotranslationsCom(item):
	'''
	Parser for 'www.kuronotranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Level Up Just By Eating" in item['tags']:
		return buildReleaseMessageWithType(item, "Level Up Just By Eating", vol, chp, frag=frag, postfix=postfix)
	if "Kou 1 Desu ga Isekai de Joushu Hajimemashita" in item['tags']:
		return buildReleaseMessageWithType(item, "Kou 1 Desu ga Isekai de Joushu Hajimemashita", vol, chp, frag=frag, postfix=postfix)

	return False