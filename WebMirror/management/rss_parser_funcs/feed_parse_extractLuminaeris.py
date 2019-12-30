def extractLuminaeris(item):
	"""
	'Luminaeris'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('PRC',                                        'PRC',                                                       'translated'),
		('Another World, Another Gender',              'Another World, Another Gender',                             'translated'),
		('vitae memorandum',                           'Vitae Memorandum',                                          'oel'),
		('Loiterous',                                  'Loiterous',                                                 'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False