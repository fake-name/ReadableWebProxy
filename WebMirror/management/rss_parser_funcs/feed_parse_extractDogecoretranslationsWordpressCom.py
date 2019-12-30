def extractDogecoretranslationsWordpressCom(item):
	'''
	Parser for 'dogecoretranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('TGNR',       'The Great Nation Remodeling of Reincarnated Princess ~Let’s Build an Unrivaled Country~',    'translated'),
		('PKAW',       'The Pseudo-Kunoichi From a Different World',                                                 'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	return False