def extractKiyoitsukikage(item):
	"""
	Parser for 'Kiyoitsukikage'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'request' in item['tags']:
		return None
	if 'Answers' in item['tags']:
		return None
		
	tagmap = [
		('Sasuke shinden',       'Sasuke Shinden',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False