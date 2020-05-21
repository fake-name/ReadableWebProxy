def extractWwwFuyunekoOrg(item):
	'''
	Parser for 'www.fuyuneko.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if item['tags'] == []:
		chp_prefixes = [
				('The Villain and the CF’s Mother - Ch ',                                          'The Villain and the Cannon Fodder’s Mother',                'translated'),
				('Pregnant with the Villain’s Child - Ch ',                                        'I’m Pregnant with the Villain’s Child',                'translated'),
				('The FSC Ran Off With the Bun - Ch ',                                             'The Female Supporting Character Ran Off With The Bun',                'translated'),
				('The Villain\'s Contract Lover - Ch ',                                            'The Villain\'s Contract Lover',                'translated'),
				('My Wife is My Life! - Ch ',                                                      'In which the System Torments the Protagonists: My Wife is My Life!',                'translated'),
				('Marrying the Soft-hearted Villain - Ch ',                                        'Marrying the Soft-hearted Villain',                'translated'),
				('Adopting and Raising ML and V - Ch ',                                            'Adopting and Raising the Male Lead and the Villain',                'translated'),
				('Spending the Villain\'s Money - Ch ',                                            'Spending the Villain\'s Money to Extend My Life',                'translated'),
				('ML’s Villainess Stepmother - Ch ',                                               'The Male Lead\'s Villainess Stepmother',                'translated'),
				('Villainess FSC Raising Her Bun - Ch ',                                           'The Villainess Female Supporting Character with a Bun',                'translated'),
				('Rebirth of the Evil MIL - Ch ',                                                  'Rebirth of the Evil Mother-In-Law',                                    'translated'),
				('ChongFei Manual Ch ',                                                            'ChongFei Manual',                                                      'translated'),
				('The Dreamer in the Spring Boudoir - Ch ',                                        'The Dreamer in the Spring Boudoir',                                    'translated'),
				('The Male Lead’s Villainess Stepmother - Ch ',                                    'The Male Lead’s Villainess Stepmother',                                'translated'),
				('Adopting and Raising the Male Lead and the Villain - Ch ',                       'Adopting and Raising the Male Lead and the Villain',                   'translated'),
				('Spending the Villain\'s Money to Extend My Life - Ch ',                          'Spending the Villain\'s Money to Extend My Life',                      'translated'),
				('The Villain and the Cannon Fodder’s Mother - Ch ',                               'The Villain and the Cannon Fodder\'s Mother',                          'translated'),
				('I’m Pregnant with the Villain’s Child - Ch ',                                    'I’m Pregnant with the Villain’s Child',                                'translated'),
				('In which the System Torments the Protagonists: My Wife is My Life! - Ch ',       'In which the System Torments the Protagonists: My Wife is My Life!',   'translated'),
				('The Villain\'s Mother - Ch ',                                                    'The Villain\'s Mother',                                                'translated'),
				('The Jilted Male Lead Hires a Mother for the Cute Shapeshifters - Ch ',           'The Jilted Male Lead Hires a Mother for the Cute Shapeshifters',       'translated'),
				('My Son Might Be A Villain - Ch ',                                                'My Son Might Be A Villain',                                            'translated'),
				('The Villain’s Younger Sister - Ch ',                                             'The Villain\'s Younger Sister',                                        'translated'),
			
				('Transmigrated into a Parvenu\'s Ex-wife in the ‘90s - Ch ',                      'Transmigrated into a Parvenu\'s Ex-wife in the \'90s',                 'translated'),
				('Parvenu\'s Ex-wife in the ‘90s - Ch ',                                           'Transmigrated into a Parvenu\'s Ex-wife in the \'90s',                 'translated'),
			]
	
		for prefix, series, tl_type in chp_prefixes:
			if item['title'].lower().startswith(prefix.lower()):
				
				# Ignore mis-parsing the series name
				if series == "Transmigrated into a Parvenu\'s Ex-wife in the ‘90s" and chp == 90:
					return None
					
				return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
 
	return False