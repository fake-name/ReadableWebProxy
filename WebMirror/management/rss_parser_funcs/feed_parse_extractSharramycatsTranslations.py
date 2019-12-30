def extractSharramycatsTranslations(item):
	"""
	'Sharramycats Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('11 Ways to Forget Your Ex-Boyfriend',       '11 Ways to Forget Your Ex-Boyfriend', 'translated'),
		('The Monster Inside Of My Bed',              'The Monster Inside Of My Bed',        'translated'),
		('The Peculiars\' Tale',                      'The Peculiars\' Tale',                'translated'),
		('ARG',                                       'A. R. G.',                            'translated'),
		('Legend of Gemini',                          'Legend of Gemini',                    'translated'),
		('Kaliskis',                                  'Kaliskis',                            'translated'),
		('She Died',                                  'She Died',                            'translated'),
		('Ice Goddess',                               'Ice Goddess',                         'translated'),
		('The Friendly Wedding',                      'The Friendly Wedding',                'translated'),
		('Forlorn Madness',                           'Forlorn Madness',                     'translated'),
		('Hidden Inside The Academy',                 'Hidden Inside The Academy',           'translated'),
		('The Señorita',                              'The Señorita',                        'translated'),
		('School Of Myths',                           'School of Myths',                     'translated'),
		('The Guys Inside of My Bed',                 'The Guys Inside of My Bed',           'translated'),
		('The Guy Inside Of My Bed',                  'The Guys Inside of My Bed',           'translated'),
		('Titan Academy Of Special Abilities',        'Titan Academy Of Special Abilities',  'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False