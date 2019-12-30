def extractTonyYonKa(item):
	"""
	# tony-yon-ka.blogspot.com (the blog title is stupidly long)

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Manowa' in item['title'] and chp:
		return buildReleaseMessageWithType(item, 'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru', vol, chp, frag=frag, postfix=postfix)
	if 'Vampire Princess' in item['title'] and chp:
		return buildReleaseMessageWithType(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
	return False
