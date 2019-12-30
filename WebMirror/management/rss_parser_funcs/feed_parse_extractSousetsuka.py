def extractSousetsuka(item):
	"""
	# Sousetsuka
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Desumachi' in item['tags'] or 'Death March kara Hajimaru Isekai Kyousoukyoku' in item['title']:
		extract = re.search('Kyousoukyoku (\\d+)\\-(\\d+)', item['title'])
		if extract and not vol:
			vol = int(extract.group(1))
			chp = int(extract.group(2))
		return buildReleaseMessageWithType(item, 'Death March kara Hajimaru Isekai Kyousoukyoku', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('Yuusha Furi',          'Yuusha no Furi mo Raku Janai --Riyuu? Ore ga Kami Dakara--',          'translated'),
		('Nobusan',              'Shinsetsu Nobu-san Isekai Ki',                                        'translated'),
		('ShikkakuMon',          'Shikkaku Mon no Saikyou Kenja',                                       'translated'),
		('Okami Nemuranai',      'Okami Wa Nemuranai',                                                  'translated'),
		
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False