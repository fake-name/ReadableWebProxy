def extractOrangeTranslations(item):
	"""
	'Orange Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Teaser' in item['tags']:
		return None
	if '1-Pg Stories' in item['tags']:
		return None
	if 'Subtitles' in item['tags']:
		return None
		
	tagmap = [
		('Buy One Get One Free',                                           '￥1 Trillion Wife, Buy One Get One Free',                      'translated'), 
		('Trillion',                                                       '￥1 Trillion Wife, Buy One Get One Free',                      'translated'), 
		('Millennium',                                                     'The Millennium After Dying Young',                             'translated'), 
		('Great God, I\'ll Support You!',                                  'Great God, I will Support You!',                               'translated'), 
		('Great God',                                                      'Great God, I will Support You!',                               'translated'), 
		('boyfriend always turned out to be a horror movie boss',          'boyfriend always turned out to be a horror movie boss',        'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False