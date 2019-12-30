def extractAoriTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'WT' in item['tags']:
		return buildReleaseMessageWithType(item, 'World Teacher - Different World Style Education Agent', vol, chp, frag=frag, postfix=postfix)
	if 'Lv2' in item['tags']:
		return buildReleaseMessageWithType(item, "Ex-Hero Candidate's, Who Turned Out To Be A Cheat From Lv2, Laid-back Life In Another World", vol, chp, frag=frag, postfix=postfix)
	return False
