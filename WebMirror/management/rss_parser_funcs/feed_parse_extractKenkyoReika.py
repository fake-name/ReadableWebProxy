def extractKenkyoReika(item):
	"""
	'Kenkyo Reika'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Botsuraku Youtei Nanode, Kajishokunin wo Mezasu',  'Botsuraku Youtei Nanode, Kajishokunin wo Mezasu', 'translated'),
		('My Death Flags Show No Sign of Ending',            'My Death Flags Show No Sign of Ending', 'translated'),
		('Hone no aru Yatsu',                                'Hone no aru Yatsu', 'translated'),
		('LV999 Villager',                                   'LV999 Villager', 'translated'),
		('amaku',                                            'Amaku Yasashii Sekai de Ikiru ni wa', 'translated'),
		('Kenkyo',                                           'Kenkyo, Kenjitsu o Motto ni Ikite Orimasu!', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False