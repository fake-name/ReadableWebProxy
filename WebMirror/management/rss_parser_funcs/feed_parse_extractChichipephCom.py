def extractChichipephCom(item):
	'''
	Parser for 'chichipeph.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the former wife',       'The Former Wife of Invisible Wealthy Man',                      'translated'),
		('villain father',       'Guide the Villain Father to Be Virtuous',                      'translated'),
		('bhwatp',       'Become Husband and Wife According To Pleasure',                      'translated'),
		('jiaochen',       'Jiaochen',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False