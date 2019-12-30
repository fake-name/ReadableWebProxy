def extractNononosanctuaryXyz(item):
	'''
	Parser for 'nononosanctuary.xyz'
	'''
	
	if 'News, Updates, ETC.' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('MaouMuji',                                                                           'I Became the Demon Lord and my Territory was an Uninhabited Island',                                'translated'),
		('I Became the Demon Lord and my Territory was an Uninhabited Island',                 'I Became the Demon Lord and my Territory was an Uninhabited Island',                                'translated'),
		('I Became the Demon Lord and my Territory was an Uninhabited Island (Nocturn)',       'I Became the Demon Lord and my Territory was an Uninhabited Island (Nocturn)',                      'translated'),
		('woof woof story',                                                                    'Woof Woof Story ~ I Told You I am a Rich Person\'s Dog, Not Fenrir ~',                              'translated'),
		('Isekai ni Kita Mitai',                                                               'It seems I came to Another World, Now What Should I Do',                                            'translated'),
		('Isekai Mitai',                                                                       'It seems I came to Another World, Now What Should I Do',                                            'translated'),
		('salty yet sweet sato-san',                                                           'Aren\'t you too sweet Salt-God Sato-san?',                                                          'translated'),
		('okaeri saotome-san',                                                                 'I\'m being paid ¥ 300,000 a month to say \'okaeri, kyo mo ganbatta ne\' to a hardworking neighbor oneesan who earns ¥500,000 a month but doesn\'t have a use for the money, which is really fun',                      'translated'),
		('sekigae bishoujo ni horerareta',                                                     'My Seatmate Tries to Make Me Fall in Love with Her by Teasing Me Repeatedly, but Somehow She Was the One Who Fell',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]
	
	if 'Nocturn' in item['title'] and not postfix:
		postfix = "Nocturn Version"
	
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False