def extractThepotatoroomCom(item):
	'''
	Parser for 'thepotatoroom.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('non-human sub-district office',                                                  'non-human sub-district office',                                                  'translated'),
		('as the demon king, i am very distressed because the hero is too weak 1.0',       'as the demon king, i am very distressed because the hero is too weak 1.0',       'translated'),
		("please respect the occupation 'evil spirit'",                                    "please respect the occupation 'evil spirit'",                                    'translated'),
		('there\'s something wrong with this development!',                                'there\'s something wrong with this development!',                                'translated'),
		('insider',                                                                        'Insider',                                                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False