def extractJadeRabbitNet(item):
	'''
	Parser for 'jade-rabbit.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('His Royal Highness, Wants A Divorce',       'His Royal Highness, Wants A Divorce',                      'translated'),
		('Nan Chan',                                  'Nan Chan',                                                 'translated'),
		('Fox Demon Cultivation Manual',              'Fox Demon Cultivation Manual',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False