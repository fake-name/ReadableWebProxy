def extractSousakuBlog(item):
	'''
	Parser for 'sousaku.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Moto Sekai Ichi',        'Moto Sekai Ichi i no sub-chara ikusei nikki ～hai player, isekai wo kouryaku chū!～',                                       'translated'),
		('maseki gurume',          'Magic Gems Gourmet',                                                                                                        'translated'),
		('High Spec Village',      'Ore no Ongaeshi: High Spec Murazukuri',                                                                                     'translated'),
		('teihen ryoushu',         'Teihen Ryoushu no Kanchigai Eiyuutan ～Heimin ni Yasashiku shite tara, Itsunomanika Kuni to Sensou ni natte ita ken～',     'translated'),
		('Looking for a Scenery',  'In search of a scenery I’ve yet to see.',                                                                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False