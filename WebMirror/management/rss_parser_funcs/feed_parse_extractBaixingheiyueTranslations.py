def extractBaixingheiyueTranslations(item):
	'''
	Parser for 'BaiXingHeiYue Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "Flash Marriage" in item['tags']:
		return buildReleaseMessageWithType(item, "Flash Marriage", vol, chp, frag=frag, postfix=postfix)

	return False