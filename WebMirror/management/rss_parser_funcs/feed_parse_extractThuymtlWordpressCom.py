def extractThuymtlWordpressCom(item):
	'''
	Parser for 'thuymtl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('tvwfil',       'The Villainess who falls in love ~The new fiance who seems to be quiet was the Ultimate Yandere~',                      'translated'),
		# ('unknown?',       'The reincarnated Princess candidate aims for a happy ending ~ Yandere / Confinement / Ahegao, No! ~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False