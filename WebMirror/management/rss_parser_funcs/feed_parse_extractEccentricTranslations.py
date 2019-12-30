def extractEccentricTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('True Immortal',    'True Immortal',                        'oel'),
		('ILK',    'Invincible Leveling King',                        'translated'),
		('ATF',    'After Transformation, Mine and Her Wild Fantasy', 'translated'),
		('DTW',    'Doctoring the World',                             'translated'),
		('TKDG',   'The Kind Death God',                              'translated'),
		('SPO',    'Single Player Only',                              'translated'),
		('VW:CCM', 'Virtual World: Close Combat Mage',                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('TKDG ',                 'The Kind Death God',                                   'translated'),
		('SPO ',                  'Single Player Only',                                   'translated'),
		('ATF ',                  'After Transformation, Mine and Her Wild Fantasy',      'translated'),
		('Doctoring the World',   'Doctoring the World',                                  'translated'),
	]

	for titlecomponent, name, tl_type in tagmap:
		if item['title'].lower().startswith(titlecomponent.lower()):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
		
	return False