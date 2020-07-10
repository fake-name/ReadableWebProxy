def extractShiroritranslationsWordpressCom(item):
	'''
	Parser for 'shiroritranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('okitara 20nen',           'Okitara 20nen nandesukedo! Akuyaku reijo no sono ato no sono ato',                                                                              'translated'),
		('seijo ni narunode',       'Seijo ni Narunode Nidoume no Jinsei wa Katte ni Sasetemoraimasu ~Outaihi wa, Zensei de Watashi wo Futta Koibito Deshita~',                      'translated'),
		('nazeboku',                'Naze Boku no Sekai wo Dare mo Oboeteinainoka?',                                                                                                 'translated'),
		('mattari',                 'Reijou wa Mattari wo Goshomou',                                                                                                                 'translated'),
		('seijuuban',               'Hikkikomori Reijou wa Hanashi no Wakaru Seijuuban',                                                                                                                 'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False