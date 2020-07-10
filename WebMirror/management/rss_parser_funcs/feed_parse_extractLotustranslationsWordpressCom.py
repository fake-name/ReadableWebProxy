def extractLotustranslationsWordpressCom(item):
	'''
	Parser for 'lotustranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	if item['tags'] == ['Announcements']:
		return None

	tagmap = [
		('Xianggong, Please Divorce Me!',               'Xianggong, Please Divorce Me!',                                'translated'),
		('100% Sweet Love',                             '100% sweet love: The delinquent XXX wife is a bit sweet',      'translated'),
		('Black Bellied President Dotes on Wife',       'Black Bellied President Dotes on Wife',                        'translated'),
		('icsaytd',                                     'I Can Still Accompany You Till Dawn',                          'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False