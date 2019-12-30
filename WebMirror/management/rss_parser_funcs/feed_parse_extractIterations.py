def extractIterations(item):
	"""
	# Iterations within a Thought-Eclipse

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'SaeKano' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)
	return False
