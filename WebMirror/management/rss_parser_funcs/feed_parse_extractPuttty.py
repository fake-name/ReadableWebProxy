def extractPuttty(item):
	"""
	# putttytranslations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if any([('god of thunder' == val.lower()) for val in item['tags']]) and (vol or chp):
		if ':' in item['title']:
			postfix = item['title'].split(':', 1)[-1]
		return buildReleaseMessageWithType(item, 'God of Thunder', vol, chp, frag=frag, postfix=postfix)
	if 'Beseech the devil'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('edge of the apocalypse',       'edge of the apocalypse',                      'translated'),
		('Goblin',                       'Goblin',                                      'translated'),
		('King of the Eternal Night',    'King of the Eternal Night',                   'translated'),
		('Martial World',                'Martial World',                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False