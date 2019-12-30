def extractIsaactranslationsWordpressCom(item):
	'''
	Parser for 'isaactranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('MotoKimama',       'The Oppressed Savior Abandons The Other World to Live As He Pleases in His Own World',                      'translated'),
		('The best assassin, incarnated into a different world\'s aristocrat',       'The best assassin, incarnated into a different world\'s aristocrat',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False