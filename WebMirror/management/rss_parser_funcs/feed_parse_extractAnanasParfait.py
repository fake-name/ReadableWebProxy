def extractAnanasParfait(item):
	"""
	Ananas Parfait
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Sorcerer Laughs in the Mirror' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Sorcerer Laughs in the Mirror', vol, chp, frag=frag, postfix=postfix)
	return False
