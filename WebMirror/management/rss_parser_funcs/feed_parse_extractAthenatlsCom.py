def extractAthenatlsCom(item):
	'''
	Parser for 'athenatls.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the second life cheat reincarnation mage',       'The Second Life Cheat Reincarnation Mage – When the strongest reincarnated after 1,000 years, his life was too much for him',                      'translated'),
		('trm',                                            'The Second Life Cheat Reincarnation Mage ~If The Strongest Reincarnated After 1000 Years, Life Would Be Too Easy~',                      'translated'),
		('the demon king of the frontier life, reincarnated to become the strongest mage',       'The Demon King Of The Frontier Life, Reincarnated To Become The Strongest Mage ~The Former Demon King Who Grows Up While Being Loved Wants To Know The Human~',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False