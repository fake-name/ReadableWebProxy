def extractRabbitcultivationCom(item):
	'''
	Parser for 'rabbitcultivation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Evil Child Black Bellied Mother',    'Evil Child Black Bellied Mother',                                          'translated'),
		('My Wayward Ex-Wife',                 'My Wayward Ex-Wife',                                                       'translated'),
		('Concubines Stunning Daughter',       'Concubine\'s Stunning Daughter : Ghost Emperor Please Be Lenient',         'translated'),
		('Concubine\'s Stunning Daughter',     'Concubine\'s Stunning Daughter : Ghost Emperor Please Be Lenient',         'translated'),
		('Loiterous',                          'Loiterous',                                                                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False