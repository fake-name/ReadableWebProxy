def extractDailyDallying(item):
	"""

	"""
	
	if 'Secret Life of Daily' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		("Notes Exchange",                 "Notes Exchange History Alteration",                    'translated'),
		("Conquering Hero's Heroines",     "Stealing Hero's Lovers",                               'translated'),
		('Nidome no Yuusha',               'Nidome no Yuusha',                                     'translated'),
		("Nobunaga's Imouto",              "Nobunaga's Younger Sister is My Wife",                 'translated'),
		('Harem Slave Master',             'Most Wicked Harem Slave Master',                       'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False