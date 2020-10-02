def extractTranslationsCraneanimeCom(item):
	'''
	Parser for 'translations.craneanime.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('my class is a lumberjack',        'Yes, My Class is “Lumberjack”, so what? ~The Giant Tree I Cut was a Mass of Exp~',                      'translated'),
		('how i become a lumberjack',       'Yes, My Class is “Lumberjack”, so what? ~The Giant Tree I Cut was a Mass of Exp~',                      'translated'),
		('young god divine armament',       'young god divine armaments',                      'translated'),
		('communicationaly challenged',      'communicationaly challenged',                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False