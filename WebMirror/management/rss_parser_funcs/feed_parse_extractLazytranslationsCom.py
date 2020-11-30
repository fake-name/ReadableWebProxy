def extractLazytranslationsCom(item):
	'''
	Parser for 'lazytranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('magic swordsman',       'The Reincarnated Inferior Magic Swordsman',                      'translated'),
		('Underground Doctor',       'Underground Doctor',                      'translated'),
		('reincarnated aristocrat',       'Reincarnated As An Aristocrat With An Appraisal Skill',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False