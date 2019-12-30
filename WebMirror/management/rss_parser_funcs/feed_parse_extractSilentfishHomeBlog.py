def extractSilentfishHomeBlog(item):
	'''
	Parser for 'silentfish.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('RMS',                              'Reincarnation of Master Su',            'translated'),
		('Reincarnation of Master Su',       'Reincarnation of Master Su',            'translated'),
		('IAAA',                             'I Am An Alpha',                         'translated'),
		('TBN',                              'Tales of the Blood Night',              'translated'),
		('WUTYO',                            'Waiting Until Thirty-five Years Old',   'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False