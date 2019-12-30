def extractXantAndMinions(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) and not 'prologue' in item['title'].lower():
		return None
		
	tagmap = [
		('coffee',                       'The Coffee Shop in a Different World Station',         'translated'),
		('iseiza',                       'Isekai Izakaya Nobu',                                  'translated'),
		('NPWC',                         'New Theory – Nobusada’s Parallel World Chronicle',     'translated'),
		('Lady Rose',                    'Lady Rose Wants to be a Commoner',                     'translated'),
		('Angel0',                       'The Angel Does Not Desire The Sky',                    'translated'),
		('Garudena',                     'Garudina Oukoku Koukoku Ki',                           'translated'),
		('Xingfeng',                     'Legend of Xingfeng',                                   'translated'),
		('Bear',                         'Kuma Kuma Kuma Bear',                                  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('LV999 Villager',                              'LV999 Villager',                                       'translated'),
		('Boundary Labyrinth and the Foreign Magician', 'Boundary Labyrinth and the Foreign Magician',          'translated'),
		('The Bears Bear a Bare Kuma',                  'Kuma Kuma Kuma Bear',                                  'translated'),
		('Kuma Kuma Kuma Bear',                         'Kuma Kuma Kuma Bear',                                  'translated'),
		('Black Knight',                                'The Black Knight Who Was Stronger than even the Hero', 'translated'),
		('Astarte’s Knight',                            "Astarte's Knight",                                     'translated'),
		('Queen’s Knight Kael',                         "Queen's Knight Kael",                                  'translated'),
		('Legend of Xingfeng',                          'Legend of Xingfeng',                                   'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False