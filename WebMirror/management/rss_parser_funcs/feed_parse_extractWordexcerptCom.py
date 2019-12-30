def extractWordexcerptCom(item):
	'''
	Parser for 'wordexcerpt.com'
	'''

	if "teaser" in item['title'].lower():
		return None
		
	procn = item['linkUrl'].replace("-", " ").replace("/", " ") + " " + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(procn)
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	

	tagmap = [
		#('InfiniteResistance',        'Infinite Resistance',                      'translated'),
		#('Infinite Resistance',       'Infinite Resistance',                      'translated'),
		#('Supreme God',               'Supreme God',                              'translated'),
		('Lady\'s Sickly Husband',                               'Lady\'s Sickly Husband',                                                           'translated'),
		('Golden Age of Phoenix',                                'Golden Age of Phoenix',                                                            'translated'),
		('Real Cheat Online',                                    'Real Cheat Online',                                                                'translated'),
		('Seirei Gensouki: Konna Sekai De Deaeta Kimi Ni',       'Seirei Gensouki: Konna Sekai De Deaeta Kimi Ni',                                   'translated'),
		('Seirei Gensouki',                                      'Seirei Gensouki: Konna Sekai De Deaeta Kimi Ni',                                   'translated'),
		('Rebirth of the Tyrant: Regent Prince Is Too Fierce',   'Rebirth of the Tyrant: Regent Prince Is Too Fierce',                               'translated'),
		('Rebirth of the Tyrant',                                'Rebirth of the Tyrant',                                                            'translated'),
		('Perfect Era',                                          'Perfect Era',                                                                      'translated'),
		('Parasite',                                             'Parasite',                                                                         'translated'),
		('Emperor\'s Might',                                     'Emperor\'s Might',                                                                 'translated'),
		('Ankoku Kishi Monogatari',                              'Ankoku Kishi Monogatari',                                                          'translated'),
		('Behemoth\'s Pet',                                      'Behemoth\'s Pet',                                                                  'translated'),
		('Rebirth of the Tyrant\'s Pet',                         'Rebirth of the Tyrant\'s Pet',                                                     'translated'),
		('(WN) Seirei Gensouki',                                 'Seirei Gensouki',                                                                  'translated'),
		('Behemoth’s Pet',                                       'Behemoth\'s Pet',                                                                  'translated'),  
		('Raising a Supporting Male Lead',                       'Guide to Raising a Supporting Male Lead',                                          'translated'),  
		('Heroes of Marvel',                                     'Heroes of Marvel',                                                                 'translated'),  
		('Number 1. Ideal Witch',                                'Second Story Online: Aiming To Become The World\'s Number 1. Ideal Witch',         'translated'),  
		('Supreme God',                                          'Supreme God',                                                                      'translated'),  
		('King Arthur',                                          'My Wife, King Arthur',                                                             'translated'),  
		('My Wife, King Arthur',                                 'My Wife, King Arthur',                                                             'translated'),  
		('I Refuse to be a Supporting Character',                'I Refuse to be a Supporting Character',                                            'translated'),  
		('Last Day On Earth',                                    'Last Days On Earth',                                                               'translated'),  
		('Refuse to be a Supporting Character',                  'I Refuse to be a Supporting Character',                                            'translated'),  
		('Quick Transmigration',                                 'Quick Transmigration: Fate Trading System',                                        'translated'),  
		('History\'s Strongest Husband',                         'History\'s Strongest Husband',                                                     'translated'),  
		('Witch Rebirth: STV',                                   'Witch Rebirth: Strike the Vampire',                                                'translated'),  
		('Bodyguard of the Goddess',                             'Bodyguard of the Goddess',                                                         'translated'),  
		('Heavenly Divine Doctor',                               'Heavenly Divine Doctor',                                                           'translated'),  
		('Our Binding Love',                                     'Our Binding Love: My Gentle Tyrant',                                               'translated'),  
		('Maouyome',                                             'Maouyome',                                                                         'translated'),  
		('PRC',       'PRC',                      'translated'),  
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	urlfrag = [
		('/series/guide-to-raising-a-supporting-male-lead/',           'Guide to Raising a Supporting Male Lead',       'translated'),
		('/series/ankoku-kishi-monogatari/',                           'Ankoku Kishi Monogatari',                       'translated'),
		('/series/real-cheat-online/',                                 'Real Cheat Online',                             'translated'),
		('/series/wn-seirei-gensouki/',                                'Seirei Gensouki (WN)',                          'translated'),
		('/series/quick-transmigration/',                              'Quick Transmigration: Fate Trading System',     'translated'),
		('/series/behemoths-pet/',                                     'Behemoth\'s Pet',                               'translated'),  
		('/series/golden-age-of-phoenix/',                             'Golden Age of Phoenix',                         'translated'),
		('/series/rebirth-of-the-tyrants-pet/',                        'Rebirth of the Tyrant\'s Pet',                  'translated'),
		('/series/desire/',                                            'Desire',                                        'translated'),  
		('/series/irsc/',                                              'I Refuse to be a Supporting Character',         'translated'),  

		('rebirth.online/novel/earths-core' ,          "Earth's Core", 'oel'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False