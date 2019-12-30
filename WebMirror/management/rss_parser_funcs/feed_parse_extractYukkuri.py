def extractYukkuri(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Nihonkoku Shoukan',                                                                                               'Nihonkoku Shoukan',                                                                     'translated'),
		('10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta',                           '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', 'translated'),
		('When I was going out from my house to stop become a Hiki-NEET after 10 years I was transported to another world', '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', 'translated'),
		('Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru',                                                          'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru',                                'translated'),
		('Tenseisha wa Cheat o Nozomanai',                                                                                  'Tenseisha wa Cheat o Nozomanai',                                                        'translated'),
		('I Won 4 Billion in a Lottery But I Went to Another World',                                                        'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru',                                'translated'),
		('Genjitsushugi Yuusha no Oukokusaikenki',                                                                          'Genjitsushugi Yuusha no Oukokusaikenki',                                                'translated'),
		('Himekishi to Camping Car',                                                                                        'Himekishi to Camping Car',                                                              'translated'),
		('A Realist Hero\'s Kingdom Reconstruction Chronicle',                                                              'A Realist Hero\'s Kingdom Reconstruction Chronicle',                                    'translated'),
		('Isekai de 『Kuro no Iyashite-tte』 Yobarete Imasu',                                                               'Isekai de 『Kuro no Iyashite-tte』 Yobarete Imasu',                                     'translated'),
		('Genjitsushugisha no Oukoku Kaizouki',                                                                             'Genjitsushugisha no Oukoku Kaizouki',                                                   'translated'),
		('The Curious Girl and The Traveler',                                                                               'The Curious Girl and The Traveler',                                                     'oel'),
		('The Primordial',                                                                                                  'The Primordial',                                                                        'oel'),
		('Yukkuri Oniisan',                                                                                                 'Yukkuri Oniisan',                                                                       'oel'),
		('The Valtras Myth',                                                                                                'The Valtras Myth',                                                                      'oel'),
		('Undeath and Taxes',                                                                                               'Undeath and Taxes',                                                                     'oel'),
		('The Bad the Worse and the Evil',                                                                                  'The Bad The Evil and The Worse',                                                        'oel'),
		('The Bad The Evil and The Worse',                                                                                  'The Bad The Evil and The Worse',                                                        'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru.',                               'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru',                                'translated'),
		('10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', 'translated'),
		('Genjitsushugi Yuusha no Oukokusaikenki.',                                               'Genjitsushugisha no Oukoku Kaizouki',                                                   'translated'),
		('Genjitsushugisha no Oukoku Kaizouki',                                                   'Genjitsushugisha no Oukoku Kaizouki',                                                   'translated'),
		('Our New World - Chapter',                                                               'Our New World',                                                                         'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	return False