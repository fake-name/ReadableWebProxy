def extractSecretlandcastleXyz(item):
	'''
	Parser for 'secretlandcastle.xyz'
	'''

	if 'Protected: ' in item['title']:
		return None
	
	badwords = [
			'Manhwa',
			'scanlation',
			'Manga',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


		

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Grand Dukes Little Lady',         'The Grand Dukes Little Lady',                        'translated'),
		('I Raised an Obsessive Servant',       'I Raised an Obsessive Servant',                      'translated'),
		('The Lady Wants to Rest',              'The Lady Wants to Rest',                             'translated'),
		('Villain&#039;s Sister',               'The Villain’s Sister is Suffering Again Today',      'translated'),
		('Devil Duke',                          'The Devil Duke\'s Little Bride',                     'translated'),
		('Hourglass',                           'The Villainess Reverses the Hourglass',              'translated'),
		('PRC', 'PRC',                'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False