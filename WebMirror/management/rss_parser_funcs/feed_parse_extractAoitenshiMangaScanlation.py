def extractAoitenshiMangaScanlation(item):
	"""
	Parser for 'Aoitenshi Manga Scanlation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Doujinshi' in item['tags']:
		return None
	if 'Akumu no Sumu Ie - Ghost Hunt' in item['tags']:
		return None
	if 'Raisekamika' in item['tags']:
		return None
	if 'Maken-Ki!' in item['tags']:
		return None
	if 'yearly digest' in item['tags']:
		return None
		
		
		
	tagmap = [
		('Warm Place',                          'Warm Place',                                         'translated'),
		('Lady Ayane is a Sanova B**chi',       'Lady Ayane is a Sanova B**chi',                      'translated'),
		('PRC',                                 'PRC',                                                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False