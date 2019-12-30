def extractNegaTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = {
		'Glutton Berserker'                : 'Glutton Berserker',
		'Kaette Kita Motoyuusha'           : 'Kaette Kita Motoyuusha',
		'Takami no Kago'                   : 'Takami no Kago',
		'Gacha Girl Corps'                 : 'Gacha Girl Corps',
		'Tanpa kategori'                   : 'Takami no Kago',
		'The Story of Hero Among Heroes'   : 'The Story of Hero Among Heroes ~The Founding Chronicles of Arestia',
		'Sono Mono, Nochi Ni'              : 'Sono Mono, Nochi Ni',
		'Arifureta'                        : 'Arifureta',
		'One-eyed female General'          : 'One-eyed Female General and the Harem',
	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
			
			
	titlemap = [
		('Takami no Kago ch',           'Takami no Kago',        'translated'),
		('Gacha Girl Corps',            'Gacha Girl Corps',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

			
			
	return False