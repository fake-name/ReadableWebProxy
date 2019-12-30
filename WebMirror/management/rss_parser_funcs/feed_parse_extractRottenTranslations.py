def extractRottenTranslations(item):
	"""
	Rotten Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Apocalypse Rebirth',                     'Apocalypse Rebirth: Chief, Don’t Move!',                'translated'),
		('Secret Service Mysterious Doctor',       'Secret Service Mysterious Doctor',                      'translated'),
		('Full-time Sponger',                      'Full-time Sponger',                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('SSMD – C. ',       'Secret Service Mysterious Doctor',                      'translated'),
		('SSMD c.',          'Secret Service Mysterious Doctor',                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False