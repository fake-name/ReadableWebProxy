def extractMulotranslationsWordpressCom(item):
	'''
	Parser for 'mulotranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Aiming For Harem Queen in Different World',                                          'Aiming For Harem Queen in Different World',                                                         'translated'),
		('TS Reincarnated as the sub heroine',                                                 'TS Reincarnated as the Sub Heroine.',                                                               'translated'),
		('I was just an only child boy, Now I became one of a four quadruplet sisters.',       'I was just an only child boy, Now I became one of a four quadruplet sisters.',                      'translated'),
		('When I became a Girl, an Unexpected Love Quarrel Occurred!',                         'When I became a Girl, an Unexpected Love Quarrel Occurred!',                                        'translated'),
		('They Said My Status Stayed the Same Even Though I Reincarnated in Another World!?',  'They Said My Status Stayed the Same Even Though I Reincarnated in Another World!?',                 'translated'),
		('emergency adaptation for a male high school put into ts.',                           'emergency adaptation for a male high school put into ts.',                                          'translated'),
		('the struggles of a young ts yuki-onna.',                                             'the struggles of a young ts yuki-onna.',                                                            'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False