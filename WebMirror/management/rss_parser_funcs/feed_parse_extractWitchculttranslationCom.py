def extractWitchculttranslationCom(item):
	'''
	Parser for 'witchculttranslation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] == ['Arc 5'] or  item['tags'] == ['Arc 6']:
		return buildReleaseMessageWithType(item, "Re:Zero − Starting Life in Another World", vol, chp, frag=frag, postfix=postfix)

	return False