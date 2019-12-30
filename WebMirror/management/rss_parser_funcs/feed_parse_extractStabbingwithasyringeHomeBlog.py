def extractStabbingwithasyringeHomeBlog(item):
	'''
	Parser for 'stabbingwithasyringe.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Reincarnated Elf Prince',                      'Harem Tales of reincarnated Elf Prince',                      'translated'),
		('Harem Tales of reincarnated Elf Prince',       'Harem Tales of reincarnated Elf Prince',                      'translated'),
		('reincarnated tower magician',                  'A Reincarnated Mage\'s Tower Dungeon Management',             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False