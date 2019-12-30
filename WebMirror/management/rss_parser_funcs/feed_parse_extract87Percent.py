def extract87Percent(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Return of the former hero' in item['tags']:
		return buildReleaseMessageWithType(item, 'Return of the Former Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon egg' in item['tags']:
		return buildReleaseMessageWithType(item, 'Reincarnated as a dragon’s egg ～Lets aim to be the strongest～', vol, chp, frag=frag, postfix=postfix)
	if 'Summoning at random' in item['tags']:
		return buildReleaseMessageWithType(item, 'Summoning at Random', vol, chp, frag=frag, postfix=postfix)
	if 'Legend' in item['tags']:
		return buildReleaseMessageWithType(item, 'レジェンド', vol, chp, frag=frag, postfix=postfix)
	if 'Death game' in item['tags']:
		return buildReleaseMessageWithType(item, 'The world is fun as it has become a death game', vol, chp, frag=frag, postfix=postfix)
	if 'Elf Tensei' in item['tags']:
		return buildReleaseMessageWithType(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag, postfix=postfix)
	return False
