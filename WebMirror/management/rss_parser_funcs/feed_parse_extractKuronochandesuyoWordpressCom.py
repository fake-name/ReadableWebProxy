def extractKuronochandesuyoWordpressCom(item):
	'''
	Parser for 'kuronochandesuyo.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Since I reincarnated・・・・" in item['tags']:
		return buildReleaseMessageWithType(item, "Since I reincarnated・・・・", vol, chp, frag=frag, postfix=postfix)

	return False