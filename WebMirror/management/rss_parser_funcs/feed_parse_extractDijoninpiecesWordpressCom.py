def extractDijoninpiecesWordpressCom(item):
	'''
	Parser for 'dijoninpieces.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Me and the Tigress ',                 'Me and the Tigress',                     'translated'),
		('I was a Sword when I Reincarnated ',  'I was a Sword when I Reincarnated',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] != ['Uncategorized']:
		return None
		
	titlemap = [
		('Tigress ',  'Me and the Tigress',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False