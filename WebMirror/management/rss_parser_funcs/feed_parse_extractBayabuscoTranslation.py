def extractBayabuscoTranslation(item):
	"""
	# 'Bayabusco Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	tagmap = [
		('Ex Strongest Swordsman', 'Former Strongest Swordsman Long For Magic In Different World',  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	

	titlemap = [
		('Demon King',                                                   'The Demon King Seems to Conquer the World',                     'translated'),
		('World Teacher',                                                'World Teacher',                                                 'translated'),
		('Tensei Shoujo no Rirekisho',                                   'Tensei Shoujo no Rirekisho',                                    'translated'),
		('Former Strongest Swordsman Long For Magic In Different World', 'Former Strongest Swordsman Long For Magic In Different World',  'translated'),
		('Ex Strongest Swordsman Longs For Magic In Different World',    'Former Strongest Swordsman Long For Magic In Different World',  'translated'),
		('Ex Strongest Swordsman Long For Magic In Different World',     'Former Strongest Swordsman Long For Magic In Different World',  'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False