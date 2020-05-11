def extractAstereadsWordpressCom(item):
	'''
	Parser for 'astereads.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Thanks to a Different World Reincarnation',       'Thanks to a Different World Reincarnation',                      'translated'),
		('s-rank appraiser',                                'The Kicked Out S-rank Appraiser',                                'translated'),
		('isekai cat',                                      'I Become a Cat in Another World',                                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	if 'level 99 villainous daughter' in item['tags'] and chp != 99:
		return buildReleaseMessageWithType(item, 'Level 99 Villainous Daughter', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
	if 'level 99 villainous' in item['tags'] and chp != 99:
		return buildReleaseMessageWithType(item, 'Level 99 Villainous Daughter', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		

	return False