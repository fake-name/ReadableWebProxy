def extractBananas(item):
	"""
	Parser for 'Bananas'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('isekai joushu chapters',                 'Struggling Hard As The Lord Of A Castle In A Different World',                                      'translated'), 
		('erufu seidorei wn',                      'The Dungeon Harem I Built With My Elf Sex Slave',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	chp_prefixes = [
			('AARASL',                          'An A-ranked Adventurer’s “Slow-living”',                             'translated'), 
			('Isekai Taneuma',                  'Isekai Taneuma',                                                     'translated'), 
			('Gang of Yuusha',                  'Gang of Yusha',                                                      'translated'), 
			('Gang of Yusha',                   'Gang of Yusha',                                                      'translated'), 
			('The Revenge of the Soul Eater',   'Soul Eater of the Rebellion',                                        'translated'), 
			('Soul Eater of the Rebellion',     'Soul Eater of the Rebellion',                                        'translated'), 
			('Sparta Teikoku ',                 'Sparta Teikoku Kenkoku Senki ',                                      'translated'), 
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False