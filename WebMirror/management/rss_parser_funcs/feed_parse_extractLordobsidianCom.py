def extractLordobsidianCom(item):
	'''
	Parser for 'lordobsidian.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	tagmap = [
		('Martial King\'s Retired Life',       'Martial King\'s Retired Life',                                     'translated'),
		('告急！重生之后的妈妈们是子控！',     'Oh No! After I Reincarnated, My Moms Became Son-cons!',            'translated'),
		('病娇魅魔女儿是勇者妈妈的天敌',       'My Yandere-Succubus Daughter is Mommy-Warrior’s Natural Enemy',    'translated'),
		('Yandere Succubus',                   'My Yandere-Succubus Daughter is Mommy-Warrior’s Natural Enemy',    'translated'),
		('MYSD',                               'My Yandere-Succubus Daughter is Mommy-Warrior’s Natural Enemy',    'translated'),
		('AATG',                               'Apotheosis – Ascension to Godhood',                                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False