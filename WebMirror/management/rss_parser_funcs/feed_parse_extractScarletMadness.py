def extractScarletMadness(item):
	"""
	Scarlet Madness
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Kanna The Godless; The Summoned Heretic Is A Scenario Breaker',                                                            'Kanna no Kanna Itanshoukansha wa Scenario Breaker',                                                                        'translated'),
		('When I was going out from my house to stop become a Hiki-NEET after 10 years I was transported to another world',          'When I was going out from my house to stop become a Hiki-NEET after 10 years I was transported to another world',          'translated'),
		('A Second Time for an Otherworld Summoning',                                                                                'A Second Time for an Otherworld Summoning',                                                                                'translated'),
		('Blessing From the Goddess and Transfer to Another World! ~No Thanks, I Already Have a Special Power~',                     'Blessing From the Goddess and Transfer to Another World! ~No Thanks, I Already Have a Special Power~',                     'translated'), 
		('Blessing from the goddess and transfer to another world! ~No thanks, I already have special power~',                       'Blessing From the Goddess and Transfer to Another World! ~No Thanks, I Already Have a Special Power~',                     'translated'), 
		('Blessing From the Goddess and Transfer to Another World! ~No Thanks, I Already Have Special Powers~',                      'Blessing From the Goddess and Transfer to Another World! ~No Thanks, I Already Have a Special Power~',                     'translated'), 
		('Corporate Slave Hero says He\'s Quitting his Job',                                                                         'Corporate Slave Hero says He\'s Quitting his Job',                                                                         'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		    
	return False