def extractEndOnline(item):
	"""

	"""
	title = item['title']
	for tag in item['tags']:
		if 'volume' in tag.lower():
			title = tag + ' ' + title
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(title)
	if not (chp or vol) or 'published' in item['title'].lower():
		return None
		
	tagmap = [
		('Eternal Anime War',        'Eternal Anime War',                       'oel'),
		('End Online',               'End Online',                              'oel'),
		('Chronicle of the Eternal', 'Chronicle of the Eternal',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False