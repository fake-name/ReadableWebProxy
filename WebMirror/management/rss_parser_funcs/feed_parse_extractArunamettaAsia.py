def extractArunamettaAsia(item):
	'''
	Parser for 'arunametta.asia'
	'''

	badwords = [
			'Menantu Sang Raja Naga',
			'Lembayung Ema',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Eiwa - The Knight of Magical Laws', 'Eiwa - The Knight of Magical Laws',                'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False