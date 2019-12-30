def extractVoidTranslations(item):
	"""
	# Void Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	match = re.search('^Xian Ni Chapter \\d+ ?[\\-–]? ?(.*)$', item['title'])
	if match:
		return buildReleaseMessageWithType(item, 'Xian Ni', vol, chp, postfix=match.group(1))
		
	tagmap = [
		('Everlasting Immortal Firmament',       'Everlasting Immortal Firmament', 'translated'),
		('Post-80s\' Cultivation Journal',       'Post-80s\' Cultivation Journal', 'translated'),
		('My Daoist Life',       'My Daoist Life', 'translated'),
		('Reaching to the Sky',  'Reaching to the Sky', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False