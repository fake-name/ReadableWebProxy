def extractBureiDan(item):
	"""
	# Burei Dan Works

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Isekai Canceller' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessageWithType(item, 'Isekai Canceller', vol, chp, frag=frag, postfix=postfix)
	if 'Kenja ni Natta' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessageWithType(item, 'Kenja ni Natta', vol, chp, frag=frag, postfix=postfix)
	if 'Han-Ryuu Shoujo no Dorei Raifu' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessageWithType(item, 'Han-Ryuu Shoujo no Dorei Raifu', vol, chp, frag=frag, postfix=postfix)
	if 'To Aru Ninki Jikkou Player no VRMMO Funtou Ki' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessageWithType(item, 'To Aru Ninki Jikkou Player no VRMMO Funtou Ki', vol, chp, frag=frag, postfix=postfix)
	return False
