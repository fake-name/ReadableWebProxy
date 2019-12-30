def extractAbsurdTranslation(item):
	"""
	Absurd Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if re.match('^I Kinda Came to Another World \\– \\d+$', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'I Kinda Came to Another World, but Where’s the Way Home?', vol, chp, frag=frag, postfix=postfix)
	if re.match('^Isekai ni Kanaderu Denset[su][su] \\– \\d+$', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'Isekai ni kanaderu densetsu ~Toki wo Tomeru Mono~', vol, chp, frag=frag, postfix=postfix)
	if re.match('^Magi’s grandson – \\d+$', item['title'], re.IGNORECASE):
		return buildReleaseMessageWithType(item, 'Magi’s Grandson', vol, chp, frag=frag, postfix=postfix)
		
	titlemap = [
		('Summoned Simultaneously to Another Worlds – ',  'Because I Was Simultaneously Summoned to Another Worlds',               'translated'),
		('Muscle Is The Best – ',                         'Magic? Muscle Is Much More Important Than Such A Thing',                'translated'),
		('Leveling Up by Walking – ',                     'Level up By Walking: in 10 thousand steps I will be level 10000',       'translated'),
		# ('Tensei Shoujo no Rirekisho',  'I Kinda Came to Another World, but Where’s the Way Home?',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False