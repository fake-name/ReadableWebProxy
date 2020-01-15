def extractPlumliziWordpressCom(item):
	'''
	Parser for 'plumlizi.wordpress.com'
	'''
	if 'Rebirth Indonesia Bahasa' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The School\'s Omnipotent Useless Garbage',       'The School\'s Omnipotent Useless Garbage',                         'translated'),
		('How Is It My Fault That I Look Like a Girl!',    'How Is It My Fault That I Look Like a Girl!',                      'translated'),
		('Hey, Don\'t Act Unruly!',                        'Hey, Don\'t Act Unruly!',                                          'translated'),
		('The Taming of the Yandere',                      'The Taming of the Yandere',                                        'translated'),
		('The Road Turns White Tonight',                   'The Road Turns White Tonight',                                     'translated'),
		('Life After Marriage',                            'Life After Marriage',                                              'translated'),
		('Pampering My Cute Pet',                          'Pampering My Cute Pet',                                            'translated'),
		('I Am a Matchmaker on Taobao',                    'I Am a Matchmaker on Taobao',                                      'translated'),
		('film empress\'s daily face slapping',            'film empress\'s daily face slapping',                              'translated'),
		('No Protection Tonight',                          'No Protection Tonight',                                            'translated'),
		('he\'s mine, no objections allowed',              'He\'s Mine, No Objections Allowed',                                'translated'),
		('rebirth',                                        'Rebirth: Noble Woman, Poisonous Concubine',                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	chp_prefixes = [
		('Life After Marriage',                                          'Life After Marriage',                         'translated'),
		('一夜婚后|Life After Marriage Chapter',                         'Life After Marriage',                         'translated'),
		('Rebirth: Noble Woman, Poisonous Concubine|重生之贵女毐妃',     'Rebirth: Noble Woman, Poisonous Concubine',   'translated'),
	]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False