def extractUnicornsGalore(item):
	"""
	'UnicornsGalore!'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('quit entourage',       'I Will Quit the Entourage of the Villainess',                      'translated'),
		('Saw a Smile',          'I Saw a Smile',                                                    'translated'),
		('Cat Invasion',         'If It’s An Invasion Of The Earth, Of Course It’ll Be Cats Right?', 'translated'),
		('Impaired hero',        'The Immortal Demon King and the Impaired Hero',                    'translated'),
		('Beauty\'s secret',     'The Beauty’s Secret',                                              'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False