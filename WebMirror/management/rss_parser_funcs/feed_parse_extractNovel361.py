def extractNovel361(item):
	"""
	Parser for 'Novel 361'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	urlfrag = [
		# I can't fucking tell what this series is!
		# ('/sohrh-chapter',  'Jintetsu',     'translated'),

	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False