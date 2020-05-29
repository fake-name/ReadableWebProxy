def extractRufftranslationsWordpressCom(item):
	'''
	Parser for 'rufftranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if frag and not (chp and vol):
		chp = frag
		frag = None
		
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		

	tagmap = [
		('the communication hero with the cool heroine',       'As the Communication Hero, I Formed the World\'s Strongest Party with a Cool Big Sister',                      'translated'),
		('the pseudo-ninja from another world',                'the pseudo-kunoichi from another world',                            'translated'),
		('the pseudo-kunoichi from another world',             'the pseudo-kunoichi from another world',                            'translated'),
		('yuri flags with the heroine',                        'When I Reincarnated as the Villainess, I Raised Yuri Flags with the Heroine!?',                                       'translated'),
		('the death flag-breaking villainess',                 'I Was Reincarnated As The Villainess Of An Otome Game, But As I Broke The Death Flags With All My Might, The Heroine Opened My Route',                                       'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False