def extractKoiTranslationsCom(item):
	'''
	Parser for 'koi-translations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('Potatoes are the only thing that’s needed in this world! Chapter ',  'Potatoes are the only thing that’s needed in this world!',      'translated'),
			('Bewitching Demonic Beast Chapter ',                                  'Bewitching Demonic Beast',                                      'translated'),
			('Becoming A Global Superstar Starting As An Idol Trainee Chapter ',  'Becoming A Global Superstar Starting As An Idol Trainee',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False