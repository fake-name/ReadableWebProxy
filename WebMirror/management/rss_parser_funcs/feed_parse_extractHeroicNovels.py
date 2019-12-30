def extractHeroicNovels(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('id',                              'ID – The Greatest Fusion Fantasy',    'translated'),
		('Magician City',                   'Magician City',                       'translated'),
		('The Hero',                        'The Hero',                            'translated'),
		('reader',                          'Reader',                              'translated'),
		('Dragon Order of Flame',           'Dragon Order of Flame',               'translated'),
		('The Overlord of Blood and Iron',  'The Overlord of Blood and Iron',      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['title'].startswith('The Hero Volume'):
		return buildReleaseMessageWithType(item, 'The Hero', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Metatron Volume'):
		return buildReleaseMessageWithType(item, 'Metatron', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Dragon Order of Flame Vol'):
		return buildReleaseMessageWithType(item, 'Dragon Order of Flame', vol, chp, frag=frag, postfix=postfix)
	return False