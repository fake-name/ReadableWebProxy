def extractIAmABananaFreshieTranslation(item):
	"""
	'IAmABanana Freshie Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('(ON)The Yin Emperor or The Yang Empress'):
		return buildReleaseMessageWithType(item, 'The Yin Emperor or The Yang Empress', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('雨露均沾 Sharing Rain and Dew –'):
		return buildReleaseMessageWithType(item, 'Sharing Rain and Dew', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('Prince You Are So Cheap' ,                 'Prince You Are So Cheap',                              'translated'),
		('GMMU' ,                                    'Good Morning, Miss Undercover',                        'translated'),
		('先撩为敬 Let me tease you' ,               'Let Me Tease You',                                     'translated'),
		('yin emperor yang empress' ,                'The Yin Emperor or The Yang Empress',                  'oel'),
		('Tribe 穿越之游兽部落',                     'Transmigrated into a Beast Tribe',                     'translated'),
		('我的室友可能不是omega Roommate Omega',     'My roommate probably is not an Omega',                 'translated'),
		('魔教卧底每天都在露馅 Evil Sect',           'Evil Cult Undercover',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False