def extractTheundeadmachinetranslatorWordpressCom(item):
	'''
	Parser for 'theundeadmachinetranslator.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Sono Mugen no Saki',                                           'Sono Mugen no Saki',      'translated'), 
		('She Professed Herself The Pupil Of The Wiseman (WN) chapter',  'She Professed Herself Pupil of a Wiseman (WN)',      'translated'), 
		('She Professed Herself Pupil of a Wiseman (WN) Chapter',        'She Professed Herself Pupil of a Wiseman (WN)',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False