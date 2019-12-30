def extractHecatesCorner(item):
	"""
	"Hecate's Corner"
	"""
	
	if 'ヘカテのオススメ' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Meido',                        'Maid will go on through thick and thin!',     'translated'),
		('HeroxMaou',                    'HeroxMaou',                                   'translated'),
		('Lightning Empress Maid',       'Lightning Empress Maid',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('L.E.M. C.',                   'Lightning Empress Maid',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False