def extractRoyalNovel(item):
	"""
	Royal Novel
	"""
	ttmp = item['title']
	ttmp = re.sub(' BK(\\d+)', ' book \\1', ttmp, flags=re.IGNORECASE)
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(ttmp)
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Hero Chronicles' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hero Chronicles', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Philippine Lore' in item['tags']:
		return buildReleaseMessageWithType(item, 'Philippine Lore', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Re:Otaku Prince life in another world' in item['tags']:
		return buildReleaseMessageWithType(item, 'Re:Otaku Prince life in another world', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'disgraced consort' in item['tags']:
		return buildReleaseMessageWithType(item, 'Disgraced Consort', vol, chp, frag=frag, postfix=postfix)
	if 'xiao hun palace' in item['tags']:
		return buildReleaseMessageWithType(item, 'Xiao Hun Palace', vol, chp, frag=frag, postfix=postfix)
	if 'favored intelligent concubine' in item['tags']:
		return buildReleaseMessageWithType(item, 'Favored Intelligent Concubine', vol, chp, frag=frag, postfix=postfix)
	if 'Abandoned Empress' in item['tags']:
		return buildReleaseMessageWithType(item, 'Phoenix Overlooking the World – Who Dares to Touch My Abandoned Empress', vol, chp, frag=frag, postfix=postfix)
	return False
