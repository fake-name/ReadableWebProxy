def extractRoxism(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Bocchi Tenseiki' in item['tags'] and 'chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Bocchi Tenseiki', vol, chp, frag=frag, postfix=postfix)
	if 'Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~' in item['tags'] and 'chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~', vol, chp, frag=frag, postfix=postfix)
	if 'DHM' in item['tags'] and 'chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Dungeon+Harem+Master', vol, chp, frag=frag, postfix=postfix)
		
		

	tagmap = [
		('Behemoth Pet',                                          'Behemoth Pet',                                                      'translated'),
		('Ankoku Kishi Monogatari',                               'Ankoku Kishi Monogatari',                                           'translated'),
		('Real Cheat Online',                                     'Real Cheat Online',                                                 'translated'),
		('Bocchi Tenseiki',                                       'Bocchi Tenseiki',                                                   'translated'),
		('NFB',                                                   'Nozomanu Fushi no Boukensha',                                       'translated'),
		('DHM',                                                   'Dungeon+Harem+Master',                                              'translated'),
		('Eiyuu 《Shuyaku》 ni Narenai Yari Tsukai',              'Eiyuu 《Shuyaku》 ni Narenai Yari Tsukai',                          'translated'),
		('Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~',       'Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~',                   'translated'),
		('Parasite',                                              'I Leveled up from Being a Parasite, But I May Have Grown Too Much', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False