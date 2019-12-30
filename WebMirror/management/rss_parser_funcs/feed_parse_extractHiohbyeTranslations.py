def extractHiohbyeTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Corpse King Confuses the World, All Seven Husbands Are Devils' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Corpse King Confuses the World, All Seven Husbands Are Devils', vol, chp, frag=frag, postfix=postfix)
		
		
	tagmap = [
		('The Corpse King Confuses the World, All Seven Husbands Are Devils',       'The Corpse King Confuses the World, All Seven Husbands Are Devils',                      'translated'),
		('Blood-Sucking Empress',                                                   'Blood-Sucking Empress',                                                                  'translated'),
		('Seventh Imperial "Brother"',                                              'Seventh Imperial "Brother"',                                                             'translated'),
		('Chang\'an Intoxicated',                                                   'Chang\'an Intoxicated',                                                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False