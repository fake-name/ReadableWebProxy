def extractWwwJustreadsNet(item):
	'''
	Parser for 'www.justreads.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('[ATP] ',                      'Accompanying the Phoenix',      'translated'),
		('[Q] ',                        'Qingge [Rebirth]',      'translated'),
		('[AOOO] ',                     'The Otherworldly Adventures of a Super Naive Girl',      'translated'),
		('[OASNG] ',                    'The Otherworldly Adventures of a Super Naive Girl',      'translated'),
		('[RJWSHH] ',                    'Rebirth: the Journey of a Wife Spoiling Her Husband',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False