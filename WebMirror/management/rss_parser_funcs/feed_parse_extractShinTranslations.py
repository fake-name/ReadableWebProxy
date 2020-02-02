def extractShinTranslations(item):
	"""
	# Shin Translations

	"""
	
	
	badwords = [
			'Status Update',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	tagmap = [
		('THE NEW GATE',                                                     'The New Gate',                                          'translated'),
		('starting a new life for the discarded all-rounder',                'Starting a New Life for the Discarded All-Rounder',     'translated'),
		('dar',                                                              'Starting a New Life for the Discarded All-Rounder',     'translated'),
		('PRC',                'PRC',                               'translated'),
		('Loiterous',          'Loiterous',                         'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False