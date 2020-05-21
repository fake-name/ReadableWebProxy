def extractNovicetranslationsWordpressCom(item):
	'''
	Parser for 'novicetranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Translations']:
		titlemap = [
			('The Little Princess Imprisoned by the Demonic Brothers Ch',  'The Little Princess Imprisoned by the Demonic Brothers',      'translated'),
			('Who moved my ashes ch',                                      'Who moved my ashes',                                          'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('this princess punishes your nine generations',               'this princess punishes your nine generations',                      'translated'),
		('the villain has blackened again',                            'the villain has blackened again',                                   'translated'),
		("don't be jealous, i will bend myself",                       "don't be jealous, i will bend myself",                              'translated'),
		('next door theres memeda',                                    'Next Door There\'s Memeda',                                         'translated'),
		('willingly baited',                                           'Willingly Baited',                                                  'translated'),
		('who moved my ashes',                                         'who moved my ashes',                                                'translated'),
		('seeking good temptation',                                    'seeking good temptation',                                           'translated'),
		('Lovable Beauty',                                             'Lovable Beauty',                                                    'translated'),
		('never dare to abuse the female protagonist again',           'never dare to abuse the female protagonist again',                  'translated'),
		('the little princess imprisoned by the demon brothers',       'the little princess imprisoned by the demon brothers',              'translated'),
		('my husband with scholar syndrome',                           'my husband with scholar syndrome',                                  'translated'),
		('chasing a flower blossom',                                   'chasing a flower blossom',                                          'translated'),
		('ah, senior brother is actually a sister!',                   'ah, senior brother is actually a sister!',                                  'translated'),
		('believe it or not, i already caught you',                    'believe it or not, i already caught you',                                   'translated'),
		('female lead, please let go of the white moonlight',          'female lead, please let go of the white moonlight',                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False