def extractTakeyourhearttranslationWordpressCom(item):
	'''
	Parser for 'takeyourhearttranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Cheat Majutsu" in item['tags']:
		return buildReleaseMessageWithType(item, "Forcing Down Fate Using Cheat Magic", vol, chp, frag=frag, postfix=postfix)
	if "Class 3-C Has A Secret" in item['tags']:
		return buildReleaseMessageWithType(item, "Class 3-C Has A Secret", vol, chp, frag=frag, postfix=postfix)
	if "異世界支配のスキルテイカー" in item['title']:
		return buildReleaseMessageWithType(item, "Isekai Shihai no Skill Taker ~Zero kara Hajimeru Dorei Harem~", vol, chp, frag=frag, postfix=postfix)

	return False