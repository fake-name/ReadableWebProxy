def extractNetorutranslationsWordpressCom(item):
	'''
	Parser for 'netorutranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('pilgrimage',       'Netorare Pilgrimage of the Saint',                                                                                                                      'translated'),
		('production',       'Perfect & Virtuous Girlfriend’s NTR Production',                                                                                                        'translated'),
		('Alicia',           'NTR Fantasy – The Empire’s Saint Alicia –',                                                                                                             'translated'),
		('Pleasant',         'Omae no neechan no ma〇Ko kimochiyo sugi.',                                                                                                              'translated'),
		('prostitution',     'Childhood friend and student council who traveled to a prostitution harem RPG! -Heroines who sell their bodies and become bitches while loving me-',    'translated'),
		('obscene',          'For whom did she become obscene',                                                                                                                       'translated'),
		('overthrow',        'It seems that innocent prayers and funny friends will overthrow the thousand-years-long reign of the Demon Lord',                                       'translated'),
		('corrupted',        'My girlfriend is corrupted by a world whose common sense has been twisted',                                                                             'translated'),
		('slaying',          'The Demon-Slaying Girl',                                                                                                                                'translated'),
		('Sofia',            'Saintess Academy Sofia – Academy story of a JC that is earnestly going through erotic fights –',                                                        'translated'),
		('mining',           'If I mined the whole life at VRMMO, it may have transited to a similar world that is similar [NTR]',                                                    'translated'),
		('Sword',            'Sexual swordsmanship dojo ~Naughty practice with beloved disciples with crotch sword~',                                                                 'translated'),
		('actress',          'My girlfriend is an AV actress',                                                                                                                        'translated'),
		('dualism',          'Dualism ~She is embraced by a male friend while loving her boyfriend~',                                                                                 'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False