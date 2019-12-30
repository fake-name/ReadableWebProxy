def extractEunietlWeeblyCom(item):
	'''
	Parser for 'eunietl.weebly.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('THIS "SUMMON KITCHEN" SKILL IS AMAZING!~AMASSING POINTS BY COOKING IN ANOTHER WORLD~ CHAPTER ',       'This "Summon Kitchen" Skill is Amazing!~Amassing Points by Cooking in Another World',                      'translated'),
			('THIS "SUMMON KITCHEN" SKILL IS AMAZING!~AMASSING POINTS BY COOKING IN ANOTHER WORLD CHAPTER ',        'This "Summon Kitchen" Skill is Amazing!~Amassing Points by Cooking in Another World',                      'translated'),
			('THIS "SUMMON KITCHEN" SKILL IS AMAZING!~AMASSING POINTS BY COOKING IN ANOTHER WORLD chapter ',        'This "Summon Kitchen" Skill is Amazing!~Amassing Points by Cooking in Another World',                      'translated'),
			('EVEN THOUGH I LEFT JUST LIKE THE SCENARIO, WHAT IS IT NOW? CHAPTER ',                                 'Shinario-dōri ni Taijō Shita no ni, Imasara Nan no Goyōdesu ka?',      'translated'),
			('EVEN THOUGH I LEFT THE SCENARIO, WHAT IS IT NOW?',                                                    'Shinario-dōri ni Taijō Shita no ni, Imasara Nan no Goyōdesu ka?',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False