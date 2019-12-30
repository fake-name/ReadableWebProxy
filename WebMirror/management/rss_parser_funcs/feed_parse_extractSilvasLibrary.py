def extractSilvasLibrary(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if "Silva's Diary - Zero no Tsukaima" in item['tags']:
		return buildReleaseMessageWithType(item, "Silva's Diary - Zero no Tsukaima", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'God of Destruction' in item['tags']:
		return buildReleaseMessageWithType(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'God of Chaos' in item['tags']:
		return buildReleaseMessageWithType(item, 'God of Chaos', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'My Path of Justice' in item['tags'] or 'MPJ1' in item['tags']:
		return buildReleaseMessageWithType(item, 'My Path of Justice', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Truth and Myths' in item['tags']:
		return buildReleaseMessageWithType(item, 'Truth and Myths', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Soft Spoken Brutality' in item['tags']:
		return buildReleaseMessageWithType(item, 'Soft Spoken Brutality', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'World of Immortals' in item['tags']:
		return buildReleaseMessageWithType(item, 'World of Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Bu ni mi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Bu ni mi', vol, chp, frag=frag, postfix=postfix)
	if 'Rinkan no Madoushi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Rinkan no Madoushi', vol, chp, frag=frag, postfix=postfix)
	if 'Arifureta' in item['tags']:
		return buildReleaseMessageWithType(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	if 'High Comprehension Low Strength' in item['tags']:
		return buildReleaseMessageWithType(item, 'High Comprehension Low Strength', vol, chp, frag=frag, postfix=postfix)
	if 'Martial Void King' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial Void King', vol, chp, frag=frag, postfix=postfix)
	if 'Very Pure and Ambiguous' in item['tags']:
		return buildReleaseMessageWithType(item, 'Very Pure and Ambiguous: The Prequel', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('The Demon King\'s Daughter',       'The Demon King\'s Daughter',                      'translated'),
		('6-Year Old Sage',                  '6-Year Old Sage',                                 'translated'),
		('Demon Sword Maiden',               'Demon Sword Maiden',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False