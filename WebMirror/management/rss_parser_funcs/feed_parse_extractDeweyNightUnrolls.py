def extractDeweyNightUnrolls(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	
	tagmap = [
		('Chaos Of Beauty',           'Chaos Of Beauty',           'translated'),
		('Jianghu Road is Curved',    'Jianghu Road is Curved',    'translated'),
		('Grabbing Your Hand Dragging You Away',    'Grabbing Your Hand Dragging You Away',    'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	
	return False