def extractForgetfulDreamer(item):
	"""
	# Forgetful Dreamer

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'ヤンデレ系乙女ゲーの世界に転生してしまったようです' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'It seems like I got reincarnated into the world of a Yandere Otome game', vol, chp, frag=frag, postfix=postfix)
	return False
