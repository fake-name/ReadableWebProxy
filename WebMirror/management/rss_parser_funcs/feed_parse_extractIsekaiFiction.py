def extractIsekaiFiction(item):
	"""
	'Isekai Fiction'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Upstart Pastry Chef' in item['tags']:
		return buildReleaseMessageWithType(item, 'Upstart Pastry Chef ~Territory Management of a Genius Pâtissier~', vol, chp, frag=frag, postfix=postfix)
	if 'pastry' in item['tags']:
		return buildReleaseMessageWithType(item, 'Upstart Pastry Chef ~Territory Management of a Genius Pâtissier~', vol, chp, frag=frag, postfix=postfix)
	if 'herscherik' in item['tags']:
		return buildReleaseMessageWithType(item, 'Herscherik: Tensei Ouji to Urei no Daikoku', vol, chp, frag=frag, postfix=postfix)
	if 'okonomiyaki' in item['tags']:
		return buildReleaseMessageWithType(item, 'Different World’s Okonomiyaki Chain Store ~Auntie from Osaka, Reborn as Beautiful Swordswoman, on A Mission to Spread Okonomiyaki!~', vol, chp, frag=frag, postfix=postfix)
	if 'The Wolf Lord\'s Lady' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Wolf Lord\'s Lady', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('Starship Officer Becomes Adventurer',       'The Starship Officer Becomes An Adventurer',                      'translated'),
		('Sono Mono Nochi ni',                        'That Person. Later on…',                                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	return False