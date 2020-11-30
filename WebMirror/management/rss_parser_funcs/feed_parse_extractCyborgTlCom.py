def extractCyborgTlCom(item):
	'''
	Parser for 'cyborg-tl.com'
	'''
	
	
	
	
	badwords = [
			'Penjelajahan',
		]
	if any([bad in item['title'] for bad in badwords]):
		return None


	badwords = [
			'bleach: we do knot always love you',
			'kochugunshikan boukensha ni naru',
			'bahasa indonesia',
			'a returner\'s magic should be special bahasa indonesia',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('duke\'s daughter (ln)',                   'duke\'s daughter (ln)',                                  'translated'),
		('irregular rebellion',                     'irregular rebellion',                                    'translated'),
		('ore wa mada, honki o dashite inai',       'ore wa mada, honki o dashite inai',                      'translated'),
		('creating a different world',              'Creating a Different World',                             'translated'),
		('burakku na kishidan no dorei ga howaitona boukensha girudo ni hikinukarete s ranku ni narimashita',       'burakku na kishidan no dorei ga howaitona boukensha girudo ni hikinukarete s ranku ni narimashita',                      'translated'),
		('ancient demon king',       'ancient demon king',                      'translated'),
		('dark empire of orega in starcraft',       'dark empire of orega in starcraft',                      'translated'),
		('sekai saikyou no maou desuga daremo toubatsushinikitekurenainode, yuusha ikusei kikan ni sennyuusuru koto ni shimashita',       'sekai saikyou no maou desuga daremo toubatsushinikitekurenainode, yuusha ikusei kikan ni sennyuusuru koto ni shimashita',                      'translated'),
		('the reincarnation magician of the inferior eyes',       'the reincarnation magician of the inferior eyes',                      'translated'),
		('king of the death in dark palace',       'king of the death in dark palace',                      'translated'),
		('Mahouka Koukou no Rettousei',       'Mahouka Koukou no Rettousei',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False