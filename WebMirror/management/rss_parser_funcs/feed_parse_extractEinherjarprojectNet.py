def extractEinherjarprojectNet(item):
	'''
	Parser for 'einherjarproject.net'
	'''
	
	badwords = [
			'traducción',
			'jap-esp',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('1ldk soshite 2jk.',       '1LDK, Soshite 2JK',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False