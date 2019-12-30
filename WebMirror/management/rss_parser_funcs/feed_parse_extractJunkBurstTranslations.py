def extractJunkBurstTranslations(item):
	"""
	'Junk Burst Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('LMAG',              '10 Years after saying “Leave this to me and go”, I Became a Legend.',              'translated'), 
		('Cut & Paste',       'Living in this World with Cut & Paste',                                            'translated'), 
		('Slime',             'Slime Tensei. Taikensha ga Youjo Elf ni Dakishimeraretemasu',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False