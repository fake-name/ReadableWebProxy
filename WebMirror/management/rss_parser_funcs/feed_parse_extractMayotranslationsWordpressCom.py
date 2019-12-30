def extractMayotranslationsWordpressCom(item):
	'''
	Parser for 'mayotranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
			('EWP',  'Evil Wang Pampers His Ghost Doctor Fei',               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
 
	chp_prefixes = [
			('EWP Chapter ',  'Evil Wang Pampers His Ghost Doctor Fei',               'translated'),
			('Manowa',  'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru',               'translated'),
			('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False