def extractHajiko(item):
	"""
	# Hajiko translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Ryuugoroshi no Sugosuhibi' in item['title'] or 'Ryuugoroshi no Sugosu Hibi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ryugoroshi no Sugosuhibi', vol, chp, frag=frag, postfix=postfix)
	return False
