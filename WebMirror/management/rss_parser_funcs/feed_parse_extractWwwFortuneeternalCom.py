def extractWwwFortuneeternalCom(item):
	'''
	Parser for 'www.fortuneeternal.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('World Game Universe',       'Dunia Game Universe',                                                                   'translated'),
		('Dunia Game Universe',       'Dunia Game Universe',                                                                   'translated'),
		('tensei jinsei',             'Cheat aru kedo mattari kurashitai《Tensei jinsei o tanoshimou!》',                      'translated'),
		('Only Me',                   'Only Me',                                                                               'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False