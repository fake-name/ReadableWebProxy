def extractShamelessOniisan(item):
	"""
	Shameless Onii-san
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('Marietta',       'Marietta-hime no Konrei', 'translated'),
		('Spear Hero',     'Yari no Yuusha no Yarinaoshi', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False