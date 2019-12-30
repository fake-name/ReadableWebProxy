def extractMengpossoupshopWordpressCom(item):
	'''
	Parser for 'mengpossoupshop.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('《黄泉客栈》Yellow Springs Inn (Zhang Xiao Qi)',       'Yellow Springs Inn (Zhang Xiao Qi)',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False