def extractZkytlWordpressCom(item):
	'''
	Parser for 'zkytl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('msm',       'A Sword Master Childhood Friend Power Harassed Me Harshly, So I Broke Off Our Relationship And Make A Fresh Start At The Frontier As A Magic Swordsman.',                      'translated'),
		('oto',       'Ototsukai wa Shi to Odoru',                      'translated'),
		('OTOTSUKAI WA SHI TO ODORU',       'Ototsukai wa Shi to Odoru',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False