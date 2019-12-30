def extractRosyspellWordpressCom(item):
	'''
	Parser for 'rosyspell.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Professional Substitute: Chapter ',   'Professional Substitute',      'translated'),
		('Professional Substitute – Chapter ',  'Professional Substitute',      'translated'),
		('Tensei Shoujo no Rirekisho',          'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',                   'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False