def extractBananas(item):
	"""
	Parser for 'Bananas'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	chp_prefixes = [
			('AARASL',                          'An A-ranked Adventurer’s “Slow-living”',                             'translated'), 
			('Isekai Taneuma',                  'Isekai Taneuma',                                                     'translated'), 
			('Gang of Yuusha',                  'Gang of Yusha',                                                      'translated'), 
			('Gang of Yusha',                   'Gang of Yusha',                                                      'translated'), 
			('Soul Eater of the Rebellion',     'Soul Eater of the Rebellion',                                        'translated'), 
			('Sparta Teikoku ',                 'Sparta Teikoku Kenkoku Senki ',                                      'translated'), 
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False