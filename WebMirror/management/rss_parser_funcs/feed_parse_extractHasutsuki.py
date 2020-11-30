def extractHasutsuki(item):
	"""
	Hasutsuki
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Kinju Tsukai',                    'Seiju no Kuni no Kinju Tsukai',                      'translated'),
		('Kurono Senki',                    'Kuro no senki',                                      'translated'),
		('Kuro no senki',                   'Kuro no senki',                                      'translated'),
		('Annals of The Flame Kingdom',     'Annals of The Flame Kingdom',                        'translated'),
		('Demon Army Staff Officer',        'Demon Army Staff Officer',                           'translated'),
		('Wortenia Senki',                  'Wortenia Senki',                                     'translated'),
		('Wortenia War',                    'Wortenia Senki',                                     'translated'),
		('kuro no senki ln',                'Kuro no Senki LN',                                   'translated'),
		('Reform',                          'Tsumi Kake Tensei Ryoushu no Kaikaku',               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	titlemap = [
		('Record of Wortenia War – ',                    'Wortenia Senki',                                     'translated'),
		('Flame Kingdom – ',                             'Annals of The Flame Kingdom',                        'translated'),
		('Demon Army Staff Officer – ',                  'Demon Army Staff Officer',                           'translated'),
		('Kuro no Senki – ',                             'Kuro no senki',                                      'translated'),
		('The Girl and The War – ',                      'The Girl and The War',                               'translated'),
		('Alexis Empire – ',                             'The Alexis Empire Chronicle',                        'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

			
	return False