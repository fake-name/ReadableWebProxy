def extractThesylthorianCom(item):
	'''
	Parser for 'thesylthorian.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Magic Academy',                 'I was reincarnated as a Magic Academy!',                      'oel'),
		('100 Luck',                      '100 Luck and the Dragon Tamer Skill!',                        'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False