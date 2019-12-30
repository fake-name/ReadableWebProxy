def extractCeLn(item):
	"""

	####################################################################################################################################################
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Seirei Gensouki' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Seirei Gensouki - Konna Sekai de Deaeta Kimi ni', vol, chp, frag=frag, postfix=postfix)
	if 'Mushi Uta' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Mushi-Uta', vol, chp, frag=frag, postfix=postfix)
	if 'Shinonome Yuuko series' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Shinonome Yuuko wa Tanpen Shousetsu o Aishite Iru', vol, chp, frag=frag, postfix=postfix)
	if 'Mismarca Koukoku Monogatari' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Mismarca Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)
	return False
