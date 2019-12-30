def extractDjurasicoBlogspotCom(item):
	'''
	Parser for 'djurasico.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Common Sense of a Dukes daughter',                        'Common Sense of a Duke\'s Daughter',                      'translated'),
		('Common Sense of a Duke\'s Daughter',                      'Common Sense of a Duke\'s Daughter',                      'translated'),
		('Koushaku Reijou no Tashinami',                            'Common Sense of a Duke\'s Daughter',                      'translated'),
		('Koushaku Reijou no Tashinami novel',                      'Common Sense of a Duke\'s Daughter',                      'translated'),
		('The adventurer who received undesired immortality',       'Unwilling Undead Adventurer',                             'translated'),
		('Garudeina Oukoku Koukoku Ki',                             'Garudeina Oukoku Koukoku Ki',                             'translated'),
		('Maidens grand summoning',                                 'Maidens grand summoning',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False