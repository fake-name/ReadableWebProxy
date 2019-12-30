def extractKeztranslationsWordpressCom(item):
	'''
	Parser for 'keztranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('FOD',     'Quickly Wear the Face of the Devil',      'translated'), 
		('ABO',     'ABO Cadets',                              'translated'), 
		('dfc',     'The First Dragon Convention',             'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('ABO Vol',      'ABO Cadets',                              'translated'), 
		('FOD Chapter',  'Quickly Wear the Face of the Devil',      'translated'), 
		('FOD Chap',     'Quickly Wear the Face of the Devil',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False