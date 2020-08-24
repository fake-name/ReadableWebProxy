def extractHimikochouWordpressCom(item):
	'''
	Parser for 'himikochou.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	tagmap = [
		('Affection: Call of the King',       'Affection: Call of the King',                      'translated'),
		('DLLB',                              'Demon-Lord’s Little Bride',                        'translated'),
		('AFP',                               'Affection: Fate of The Pair',                      'translated'),
		('TATEV',                             'Tengu-sama And The Eternal Vow',                   'translated'),
		('MD',                                'Mating Desire',                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	chp_prefixes = [
			('SNITIP-',  'Secret Nights in the Inner Palace-Supreme Emperor and his beloved two flowered princess-',               'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False