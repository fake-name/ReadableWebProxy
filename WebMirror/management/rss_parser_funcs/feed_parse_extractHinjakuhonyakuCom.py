def extractHinjakuhonyakuCom(item):
	'''
	Parser for 'hinjakuhonyaku.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('hellmode',                                              'hellmode',                                                             'translated'),
		('the sole monster tamer in the world',                   'the sole monster tamer in the world',                                  'translated'),
		('the tale of the teapot hero\'s revenge',                'he tale of the teapot hero\'s revenge',                                'translated'),
		('my reality is a romance game',                          'my reality is a romance game',                                         'translated'),
		('rose princess of hellrage',                             'rose princess of hellrage',                                            'translated'),
		('a maiden\'s unwanted heroic epic',                      'a maiden\'s unwanted heroic epic',                                     'translated'),
		('transition to another world, landmines included',       'transition to another world, landmines included',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False