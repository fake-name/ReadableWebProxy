def extractNovelSaga(item):
	"""
	'Novel Saga'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Dragon Martial Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Martial Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Genius Sword Immortal' in item['tags']:
		return buildReleaseMessageWithType(item, 'Genius Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'Martial God Space' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Otherworldly Evil Monarch' in item['tags']:
		return buildReleaseMessageWithType(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)
	if 'Reborn as a Divine Prodigal' in item['tags']:
		return buildReleaseMessageWithType(item, 'Reborn as a Divine Prodigal', vol, chp, frag=frag, postfix=postfix)
	if "The Beast's Blood Boils" in item['tags']:
		return buildReleaseMessageWithType(item, "The Beast's Blood Boils", vol, chp, frag=frag, postfix=postfix)
	if 'The Brilliant Era' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Brilliant Era', vol, chp, frag=frag, postfix=postfix)
	if 'Ze Tian Ji' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)
	if 'Transcending The Nine Heavens' in item['tags']:
		return buildReleaseMessageWithType(item, 'Transcending The Nine Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'Heavenly Monarch', vol, chp, frag=frag, postfix=postfix)
	if 'God of Destruction' in item['tags']:
		return buildReleaseMessageWithType(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False