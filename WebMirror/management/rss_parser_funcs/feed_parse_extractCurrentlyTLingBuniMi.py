def extractCurrentlyTLingBuniMi(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('[BNM]'):
		return buildReleaseMessageWithType(item, 'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('[DD]'):
		return buildReleaseMessageWithType(item, 'Doll Dungeon', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('[HCLS]'):
		return buildReleaseMessageWithType(item, 'High Comprehension Low Strength', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('Abyss Domination',                 'Abyss Domination',           'translated'),
		('Nine Yang Sword Saint',            'Nine Yang Sword Saint',      'translated'),
		('Mysterious World Beast God',       'Mysterious World Beast God', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False