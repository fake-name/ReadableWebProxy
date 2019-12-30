def extractTheOtherHalfofMyApple(item):
	"""
	'The Other Half of My Apple'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Random' in item['tags']:
		return None
		

	tagmap = [
		('To Our Youth that is Fading Away',       'To Our Youth that is Fading Away', 'translated'),
		('Don\'t Turn From Summer',                'Don\'t Turn From Summer',          'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	chp_prefixes = [
			('To Our Youth that is Fading Away: ',    'To Our Youth that is Fading Away', 'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False