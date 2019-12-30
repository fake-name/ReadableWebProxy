def extractNovelslandingCom(item):
	'''
	Parser for 'novelslanding.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Raising a Fox Spirit in My Home',            'Raising a Fox Spirit in My Home',                           'translated'),
		('The Village Doctress',                       'The Village Doctress',                                      'translated'),
		('A Rural life in the 70s',                    'A Rural life in the 70s',                                   'translated'),
		('Love You from the Depths of the Stars',      'Love You from the Depths of the Stars',                     'translated'),
		('Life With You',                              'Life With You',                                             'translated'),
		('Chronicles of the Kingdom of Heaven',        'Chronicles of the Kingdom of Heaven',                       'translated'),
		('Miracle-working Doctor',                     'Miracle-working Doctor',                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False