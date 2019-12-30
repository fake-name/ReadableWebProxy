def extractRuinohonyakuWordpressCom(item):
	'''
	Parser for 'ruinohonyaku.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('kondo wa zettai ni jama shimasen!',              'I Swear I Won\'t Bother You Again!',                      'translated'),
		('I won\'t be a bother for sure this time!',       'I Swear I Won\'t Bother You Again!',                      'translated'),
		('今度は絶対に邪魔しませんっ！',                   'I Swear I Won\'t Bother You Again!',                      'translated'),
		('Haikei Heika, Nidome no Ouhii wa Okotowari',     'Haikei Heika, Nidome no Ouhii wa Okotowari',              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False