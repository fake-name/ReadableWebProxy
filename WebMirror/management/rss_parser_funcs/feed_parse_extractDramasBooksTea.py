def extractDramasBooksTea(item):
	"""

	"""
	

	badwords = [
			'Book Recap',
			'Drama Recaps',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		("I Don't Like This World I Only Like You", "I Don't Like This World I Only Like You",                      'translated'),
		('The Youthful You Who Was So Beautiful',   'The Youthful You Who Was So Beautiful',                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False