def extractWwwVerdantloreCom(item):
	'''
	Parser for 'www.verdantlore.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('monarch of the dark nights',                   'Monarch of the Dark Nights',                                  'translated'),
		('The Lame Daoist Priest',                       'The Lame Daoist Priest',                                      'translated'),
		('BUSS',                                         'As Beautiful as Ever, the Bells Sound under the Starry Sky',  'translated'),
		('My Wife is the Martial Alliance Leader',       'My Wife is the Martial Alliance Leader',                      'translated'),
		('tvhss',                                        'The Villain Has Something to Say',                            'translated'),
		('the final theocracy',                          'The Final Theocracy',                                         'translated'),
		('the god slaying sword brynhildr',              'the god slaying sword brynhildr',                             'translated'),
		('tales of distractions',                         'Tales of Distraction',                                        'translated'),
		('Tales of Distraction',                         'Tales of Distraction',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False