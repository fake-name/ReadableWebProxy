def extractThetranslationsargeantWordpressCom(item):
	'''
	Parser for 'thetranslationsargeant.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('TD Chapter ',                       'Fun Territory Defense of the Easy-Going Lord ~The Nameless Village Is Made Into the Strongest Fortified City by Production Magic~',                      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('let\'s raise the abandoned cat heroes',       'Let’s Raise the Abandoned Cat Heroes – An Awesome Demon Hunter Became a Teacher, and Is Missed by His S-Rank Pupils',                      'translated'),
		
		('fun territory defense',                       'Fun Territory Defense of the Easy-Going Lord ~The Nameless Village Is Made Into the Strongest Fortified City by Production Magic~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False