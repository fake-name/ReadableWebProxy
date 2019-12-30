def extractKaritranslationsWordpressCom(item):
	'''
	Parser for 'karitranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('High Spec Village',                 'Ore no Ongaeshi: High Spec Murazukuri',                                                                     'translated'),
		('Mistaken for the Demon King',       'The world’s only Demon User – I was mistaken for the Demon King after changing jobs.',                      'translated'),
		('My wish was...',                    'My Wish was…',                                                                                              'translated'),
		('The villainous girl is fine alone', 'The Villainous Noble Daughter is Perfectly Fine Alone!',                                                    'translated'),
		('Tou no Madoushi',                   'Tou no Madoushi',                                                                                           'translated'),
		('Moto Sekai Ichi',                   'Moto Sekai Ichi',                                  'translated'),
		('teihen ryoushu',                    'Teihen Ryoushu',                      'translated'),
		('maseki gurume',                     'Maseki gurume ~ mamono no chikara o tabeta ore wa saikyō!~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False