def extractNoviceTranslator(item):
	"""
	# 'NoviceTranslator'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Martial God Space Chapter' in item['title'] or 'Martial God Space' in item['tags']:
		return buildReleaseMessageWithType(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Martial Emperor Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Genius Sword Immortal' in item['tags']:
		return buildReleaseMessageWithType(item, 'Genius Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'God of Destruction' in item['tags']:
		return buildReleaseMessageWithType(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
