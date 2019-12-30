def extractCubbyfoxSite(item):
	'''
	Parser for 'cubbyfox.site'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Sweet Pampering',                  'Hidden Marriage Sweet Pampering: The Conglomerate’s Little Wife',                      'translated'),
		('Bad Girl Xiaomei',                 'Yin Xiaomei The Bad girl',                                                             'translated'),
		('Poisonous Empress Dowagers',       'The Enchanting Empress Dowager is Really Poisonous',                                   'translated'),
		('MTL Sweet Pampering',              'Hidden Marriage Sweet Pampering: The Conglomerate’s Little Wife',                      'translated'),
		('empress d0wager mtl',              'The Enchanting Empress Dowagers so Poisonous Introduction',                            'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False