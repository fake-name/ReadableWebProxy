def extractWwwLnovelreaderCom(item):
	'''
	Parser for 'www.lnovelreader.com'
	'''
	if 'TNZKMA' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Four Ikemen',       'Yonin no Ikemen ni Kyuuai sarete Ore wa Namidamedesu',                      'translated'),
		('otome game',        'YoninDare Ga Otome Geemu Dato Itta! ',                                      'translated'),
		('VD',                'Akuyaku Reijou No Yume Watari',                                             'translated'),
		# ('TNZKMA',                'Akuyaku Reijou No Yume Watari',                                             'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False