def extractDustToRust(item):
	"""
	Parser for 'Dust to Rust'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Kyuuketsu Hime' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
	if 'Vampire Princess' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
	if 'Reincarnate into a Slime' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	if 'Slime' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	return False