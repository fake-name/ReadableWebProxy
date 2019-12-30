def extractRanonetworkCom(item):
	'''
	Parser for 'ranonetwork.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Reincarnated as a Dark Elf ~The strongest magician conquers a parallel world~',       'Reincarnated as a Dark Elf ~The strongest magician conquers a parallel world~',                      'translated'),
		('The Deadbeat Master and Genius Disciple’s Misunderstood Workshop',                    'The Deadbeat Master and Genius Disciple’s Misunderstood Workshop',                                   'translated'),
		('Shingan no Yuusha',                                                                   'Shingan no Yuusha',                                                                                  'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False