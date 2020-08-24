def extractCleverneckoHomeBlog(item):
	'''
	Parser for 'clevernecko.home.blog'
	'''
	

	badwords = [
			'movie review',
			'badword',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('your husband’s leg is broken',                      'your husband’s leg is broken',                                   'translated'),
		('the case of the 27 knife stabs',                    'the case of the 27 knife stabs',                                   'translated'),
		('Fate',                                              'Fate, something so wonderful',                                   'translated'),
		('kimi no shiawase wo negatteita',                    'kimi no shiawase wo negatteita',                                   'translated'),
		('warm waters',                                       'warm waters',                                                      'translated'),
		('after being marked by a powerful love rival',       'after being marked by a powerful love rival',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False