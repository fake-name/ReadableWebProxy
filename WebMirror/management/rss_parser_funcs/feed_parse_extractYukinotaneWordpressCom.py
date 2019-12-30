def extractYukinotaneWordpressCom(item):
	'''
	Parser for 'yukinotane.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('Repair Skill: Chapter ',   'My【Repair】Skill Became an Almighty Cheat Skill, so I Thought I’d Open up a Weapon Shop',      'translated'),
			('Hazure Potion: Chapter ',  'I Decided to Start Cooking Since I Found Out the Losing Potion was Soy Sauce',                  'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False