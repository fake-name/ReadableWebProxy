def extractXaiomogetranslationWordpressCom(item):
	'''
	Parser for 'xaiomogetranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Mechanical God Emperor',  'Mechanical God Emperor',      'translated'),
		('Unfathomable Doomsday',   'Unfathomable Doomsday',       'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False