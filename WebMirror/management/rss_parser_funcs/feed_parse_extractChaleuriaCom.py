def extractChaleuriaCom(item):
	'''
	Parser for 'chaleuria.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('TLCPS',       'The Long Chase for the President’s Spouse',                      'translated'),
		('UTDS',        'Urban Tales of Demons and Spirits',                              'translated'),
		('RIAH',        'Reborn into a Hamster for 233 Days',                             'translated'),
		('rdf',         'Records of the Dragon Follower',                                 'translated'),
		('RDF',         'Records of the Dragon Follower',                                 'translated'),
		('nmd',         'No Money to Divorce',                                            'translated'),
		('ipc',         'Interstellar Power Couple',                                      'translated'),
		('fs',          'Fake Slackers',                                                  'translated'),
		('aol',         'World Hopping: Avenge Our Love',                                 'translated'),
		('DITA',        'Deep in the Act',                                                'translated'),
		('CGPA',        'The Complete Guide to the Use and Care of a Personal Assistant', 'translated'),
		('RDE',         'Rest in a Demon\'s Embrace',                                     'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False