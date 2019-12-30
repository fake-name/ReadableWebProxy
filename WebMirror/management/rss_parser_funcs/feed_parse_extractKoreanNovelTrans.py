def extractKoreanNovelTrans(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag):
		return False
	if 'Novel: Kill the Lights' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kill the Lights', vol, chp, frag=frag, postfix=postfix)
	if 'Novel: Black Butterfly' in item['tags']:
		return buildReleaseMessageWithType(item, 'Black Butterfly', vol, chp, frag=frag, postfix=postfix)
	if 'NL Novel: Our House Pet' in item['tags']:
		return buildReleaseMessageWithType(item, 'Our House Pet', vol, chp, frag=frag, postfix=postfix)
	return False
