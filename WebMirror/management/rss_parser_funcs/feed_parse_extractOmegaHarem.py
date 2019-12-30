def extractOmegaHarem(item):
	"""
	# Omega Harem Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol):
		return False
	if 'preview' in item['title']:
		return False
		
	if  're-Translations rehost' in item['tags']:
		item['srcname'] = 'Re:Translations'
		 
	if 'eliza chapter' in item['title'].lower() or 'elisa chapter' in item['title'].lower():
		if '–' in item['title'] and not postfix:
			postfix = item['title'].split('–')[-1]
		return buildReleaseMessageWithType(item, 'I Reincarnated as a Noble Girl Villainess, but why did it turn out this way', vol, chp, frag=frag, postfix=postfix)
		

	tagmap = [
		('Kokugensou',       'Kokugensou wo Item Cheat de Ikinuku (LN)',                      'translated'),
		('GunOta',       'Gun-Ota ga Mahou Sekai ni Tensei Shitara, Gendai Heiki de Guntai Harem wo Tsukucchaimashita!?',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('NEET chapter ',                              'NEET receives a dating sim game leveling system',                                                              'translated'),
		('Higawari Teni Chapter',                      'Higawari Teni ~ Ore wa Arayuru Sekai de Musou Suru ~',                                                         'translated'),
		('Destruction Flag Noble Girl Villainess',     'Destruction Flag Otome',                                                                                       'translated'),
		('Destruction Flag Otome',                     'Destruction Flag Otome',                                                                                       'translated'),
		('Demon King Reincarnation',                   'I, the Demon King, have become a noble girl villainess? Hah, what a joke.',                                    'translated'),
		('Slave Girl –',                               'Demotion Trip ~The Magic Girl Swordsman from the Hero’s Party Stumbled into Another World and Became a Slave', 'translated'),
		('Flight of the Dragon, Dance of the Phoenix', 'Dragon Flies Phoenix Dances',                                                                                  'translated'),
		('Dragon Life',                                'Dragon Life',                                                                                                  'translated'),
		('World Teacher',                              'World Teacher - Isekaishiki Kyouiku Agent',                                                                    'translated'),
		('jashin sidestory',                           'Evil God Average – Side Story',                                                                                'translated'),
		('Jashin Average Side Story',                  'Evil God Average – Side Story',                                                                                'translated'),
		('Heibon',                                     'E? Heibon Desu yo??',                                                                                          'translated'),
		('Villainess Brother Reincarnation',           'Villainess Brother Reincarnation',                                                                             'translated'),
		('The Black Knight',                           'The Black Knight Who Was Stronger than Even the Hero',                                                         'translated'),
		('Different world gender change',              'It Seems That I\'ve Slipped Into a Different World. Also, My Gender Has Changed.',                             'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False