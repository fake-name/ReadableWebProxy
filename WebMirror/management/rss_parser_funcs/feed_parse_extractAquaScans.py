def extractAquaScans(item):
	"""

	"""
	if 'Manga' in item['tags']:
		return None
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	bad_tags = [
			'Majo no Shinzou',
			'Kanata no Togabito ga Tatakau Riyuu',
			'Usotsuki Wakusei',
			'Shichifuku Mafia',
			'Rose Guns Days',
			'Dangan Honey',
			'Komomo Confiserie',
			'Moekoi',
			'Higan no Ishi',
		]
	if any([bad in item['tags'] for bad in bad_tags]):
		return None
		
	tagmap = [
		('Okobore Hime to Entaku no Kishi',       'Okoborehime to Entaku no Kishi',                      'translated'), 
		('Sugar Apple Fairy Tale',                'Sugar Apple Fairy Tale',                              'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False