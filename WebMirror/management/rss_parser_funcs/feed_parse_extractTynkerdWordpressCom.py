def extractTynkerdWordpressCom(item):
	'''
	Parser for 'tynkerd.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Amaterasu wa Kaku Katariki',             'Amaterasu wa Kaku Katariki',                            'translated'),
		('Shinshi na Orc wo Mezashimasu',          'Shinshi na Orc wo Mezashimasu',                         'translated'), 
		('Beauty, Sage and the Devil\'s Sword',    'Beauty, Sage and the Devil\'s Sword',                   'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False