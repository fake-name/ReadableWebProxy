def extractKimamanitranslateTumblrCom(item):
	'''
	Parser for 'kimamanitranslate.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	
	badwords = [
			'senyuu',
			'ask',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None

		
	tagmap = [
		('An Observation Record of my Fiancée - A Self-Proclaimed Villainess',                              'An Observation Record of my Fiancée - A Self-Proclaimed Villainess',                                             'translated'), 
		('I Reincarnated into an Otome Game as a Villainess With Only Destruction Flags…',                  'I Reincarnated Into an Otome Game as a Villainess with Only Destruction Flags...',                               'translated'), 
		('I Reincarnated Into an Otome Game as a Villainess with Only Destruction Flags...',                'I Reincarnated Into an Otome Game as a Villainess with Only Destruction Flags...',                               'translated'), 
		('The Heavily Armoured Noble Girl Monette: How To Break a Curse You Don\'t Remember Casting',       'The Heavily Armoured Noble Girl Monette: How To Break a Curse You Don\'t Remember Casting',                      'translated'), 
		('Someone Please Explain This Situation',                                                           'Someone Please Explain This Situation! The Antics of Duke Physalis',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False