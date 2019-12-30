def extractZelskytranslationsWordpressCom(item):
	'''
	Parser for 'zelskytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	tagmap = [
		('Reverend Insanity',       'Reverend Insanity',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Reverend Insanity Chapter',               'Reverend Insanity',                      'translated'), 
		('Mysterious Hidden Journey Chapter',       'Mysterious Hidden Journey',              'translated'), 
		('Necromancer’s Guide To Magic Chapter ',   'Necromancer\'s Guide To Magic',          'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False