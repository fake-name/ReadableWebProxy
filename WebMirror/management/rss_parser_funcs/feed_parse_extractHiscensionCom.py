def extractHiscensionCom(item):
	'''
	Parser for 'hiscension.com'
	'''
	if item['title'].startswith("Protected: "):
		return None
	if 'Rant-dom' in item['tags']:
		return None
		

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('MWFW',       'Bringing Modern Weapons to a Fantasy World',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False