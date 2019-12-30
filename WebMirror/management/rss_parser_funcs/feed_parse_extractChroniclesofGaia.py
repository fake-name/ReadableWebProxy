def extractChroniclesofGaia(item):
	"""
	'Chronicles of Gaia'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Dawn Traveler',                               'Dawn Traveler',                                              'translated'),
		('The Dungeon Demon Lord is the Weakest',       'The Dungeon Demon Lord is the Weakest',                      'translated'),
		('Elqueeness',                                  'Spirit King Elqueeness',                                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False