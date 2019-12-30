def extractNovelsNao(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().strip().startswith('king shura, chapter'):
		return buildReleaseMessageWithType(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().strip().startswith('devouring the heavens chapter'):
		return buildReleaseMessageWithType(item, 'Devouring the Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'Martial God Space' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Martial Peak' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	if 'Mythical Tyrant' in item['tags']:
		return buildReleaseMessageWithType(item, 'Mythical Tyrant', vol, chp, frag=frag, postfix=postfix)
	if 'Genius Sword Immortal' in item['tags']:
		return buildReleaseMessageWithType(item, 'Genius Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'King Shura' in item['tags']:
		return buildReleaseMessageWithType(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if 'Juvenile Medical God' in item['tags']:
		return buildReleaseMessageWithType(item, 'Juvenile Medical God', vol, chp, frag=frag, postfix=postfix)
	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Devouring The Heavens' in item['tags']:
		return buildReleaseMessageWithType(item, 'Devouring The Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Martial Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Martial Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Three Marriages' in item['tags']:
		return buildReleaseMessageWithType(item, 'Three Marriages', vol, chp, frag=frag, postfix=postfix)
	if 'I Fell and Thus I Must Rise Again!' in item['tags']:
		return buildReleaseMessageWithType(item, 'I Fell and Thus I Must Rise Again!', vol, chp, frag=frag, postfix=postfix)
	if 'Ascending the Heavens' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ascending the Heavens', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Unseeing Eyes' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Unseeing Eyes', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Gemstone Chronicles' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Gemstone Chronicles', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Apocalypse Now' in item['tags']:
		return buildReleaseMessageWithType(item, 'Apocalypse Now', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'God of Destruction' in item['tags']:
		return buildReleaseMessageWithType(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Song of Swords' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Song of Swords', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if "Dragon's Soul" in item['tags']:
		return buildReleaseMessageWithType(item, "Dragon's Soul", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
