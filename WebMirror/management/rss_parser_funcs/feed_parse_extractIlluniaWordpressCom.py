def extractIlluniaWordpressCom(item):
	'''
	Parser for 'illunia.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('blindness',                                                                 'Blindness',                                                                                'translated'),
		('Goddess, Help Me!',                                                         'Goddess, Help Me!',                                                                        'translated'),
		('The Sweet Side of Mister Wolf',                                             'The Sweet Side of Mister Wolf',                                                            'translated'),
		('Continuation of the Dream in Another World',                                'Continuation of the Dream in Another World',                                               'translated'),
		('Prince Takatsuki\'s Mind is Coloured Pink',                                 'Prince Takatsuki\'s Mind is Coloured Pink',                                                'translated'),
		('Troubled Villainous Daughter, My Fiancé Won’t Stop Approaching Me!?',       'Troubled Villainous Daughter, My Fiancé Won’t Stop Approaching Me!?',                      'translated'),
		('In Regards to My Second Trip and My 7 Husbands',                            'In Regards to My Second Trip and My 7 Husbands',                                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False