def extractSheeptranslator(item):
	'''
	Parser for 'SheepTranslator'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Commushou no Ore ga, Koushou Skill ni Zenfurishite Tenseishita Kekka',       'Commushou no Ore ga, Koushou Skill ni Zenfurishite Tenseishita Kekka',                      'translated'),
		('Pretty Girl Wants to Become a Good Girl',       'Pretty Girl Wants to Become a Good Girl',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]
    
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('How to Live in a Different World Chapter',                          'How to Live in a Different World',                                'translated'),
		('That Day The World Changed – Chapter',                              'That Day The World Changed',                                      'translated'),
		('That Day The World Changed Chapter',                                'That Day The World Changed',                                      'translated'),
		('Aim the Deepest Part of the Different World Labyrinth (WN)',        'Aim the Deepest Part of the Different World Labyrinth (WN)',      'translated'),
		('Arcadia’s Labyrinth Chapter',                                       'Arcadia\'s Labyrinth',                                            'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if item['title'].lower().startswith(titlecomponent.lower()):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False