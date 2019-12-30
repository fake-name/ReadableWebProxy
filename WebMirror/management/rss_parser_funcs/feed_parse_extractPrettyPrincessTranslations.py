def extractPrettyPrincessTranslations(item):
	'''
	Parser for 'Pretty Princess Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "Maouyome" in item['tags']:
		return buildReleaseMessageWithType(item, "Maou ~ Sou da, Yuusha wo Yome ni shiyou ~", vol, chp, frag=frag, postfix=postfix)
	if "Muyoku no Seijo" in item['tags']:
		return buildReleaseMessageWithType(item, "Muyoku no Seijo", vol, chp, frag=frag, postfix=postfix)

	return False