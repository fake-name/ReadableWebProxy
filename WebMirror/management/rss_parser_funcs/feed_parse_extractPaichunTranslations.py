def extractPaichunTranslations(item):
	"""
	Paichun Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		

	tagmap = [
		('Ore ga Suki nano wa Imouto dakedo Imouto ja Nai',                                 'Ore ga Suki nano wa Imouto dakedo Imouto ja Nai',                                'translated'),
		('Kenshi o Mezashite Nyūgaku Shitanoni Mahō Tekisei 9999 Nandesukedo! ?',           'Kenshi o Mezashite Nyūgaku Shitanoni Mahō Tekisei 9999 Nandesukedo! ?',          'translated'),
		('Lottery Grand Prize: Musou Harem Rights',                                         'Lottery Grand Prize: Musou Harem Rights',                                        'translated'),
		('Manga wo Yomeru Ore ga Sekai Saikyou ~Yometachi to Sugosu Ki mama na Seikatsu~',  'Manga wo Yomeru Ore ga Sekai Saikyou ~Yometachi to Sugosu Ki mama na Seikatsu~', 'translated'),
		('Ore Dake Kaereru Kurasu Teni',                                                    'Ore Dake Kaereru Kurasu Teni',                                                   'translated'),
		('Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu.',              'Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu.',             'translated'),
		('Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu.',              'Itai no wa Iya nanode Bōgyo-Ryoku ni Kyokufuri Shitai to Omoimasu.',             'translated'),
		('Kujibiki Tokushou: Musou Hāremu ken',                                             'Kujibiki Tokushou: Musou Hāremu ken',                                            'translated'),
		('Buta Kōshaku ni Tensei Shitakara, Kondo wa Kimi ni Suki to Iitai',                'Buta Kōshaku ni Tensei Shitakara, Kondo wa Kimi ni Suki to Iitai',               'translated'),
		('Hon Issatsu de Kototariru Isekai Rurō Monogatari',                                'Hon Issatsu de Kototariru Isekai Rurō Monogatari',                               'translated'),
		('Isekai Yakkyoku',                                                                 'Parallel World Pharmacy',                                                        'translated'),
		('Kyou Kara Ore wa Loli no Himo!',                                                  'Kyou Kara Ore wa Loli no Himo!',                                                 'translated'),
		('The Simple-Looking Sword Saint is Nevertheless the Strongest',                    'The Simple-Looking Sword Saint is Nevertheless the Strongest',                   'translated'),
		('The Dungeon Seeker',                                                              'The Dungeon Seeker',                                                             'translated'),
		('Tales of Leo Attiel',                                                             'Tales of Leo Attiel ~Depiction of the Headless Prince~',                         'translated'),
		('The Duke’s Daughter is the Knight Captain’s (62) Young Wife',                     'The Duke’s Daughter is the Knight Captain’s (62) Young Wife',                    'translated'),
		('Tondemo Skill de Isekai Hourou Meshi',                                            'Tondemo Skill de Isekai Hourou Meshi',                                           'translated'),
		('Level Up Just By Eating',                                                         'Level Up Just By Eating',                                                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False