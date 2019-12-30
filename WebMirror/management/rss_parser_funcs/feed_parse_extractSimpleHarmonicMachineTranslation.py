def extractSimpleHarmonicMachineTranslation(item):
	'''
	Parser for 'Simple Harmonic Machine Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Isekai Cheat Magician',      'Isekai Cheat Magician',                                               'translated'),
		('Isekai Nonbiri Nouka',       'Isekai Nonbiri Nouka',                                                'translated'),
		('Item Cheat',                 'Kokugensou wo Item Cheat de Ikinuku',                                 'translated'),
		('IFANIAW',                    'After a Different World Transition, I Founded a Nation in a Week',    'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['title'].startswith("Chapter ") and item['tags'] == ['Uncategorized']:
		return buildReleaseMessageWithType(item, "Kokugensou wo Item Cheat de Ikinuku (WN)", vol, chp, frag=frag, postfix=postfix)

	titlemap = [
		('After a Different World Transition, I Founded a Nation in a Week – C',         'After a Different World Transition, I Founded a Nation in a Week',      'translated'),
		('After a Different World Transition, I Founded a Nation in a Week – Chapter ',  'After a Different World Transition, I Founded a Nation in a Week',      'translated'),
		('The Strongest Guild Master Founded a Nation in a Week – C',                    'After a Different World Transition, I Founded a Nation in a Week',      'translated'),
		('Isekai Nonbiri Nouka – Chapter',                                               'Isekai Nonbiri Nouka',                                                  'translated'),
		('Kokugensou Wo Item Cheat de Ikinuku',                                          'Kokugensou wo Item Cheat de Ikinuku',                                   'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	if 'A Different World Scenery View From the Tower – C' in item['title']:
		match = re.search('C(\\d+)\\-(\\d+)', item['title'])
		if match:
			chp = match.group(1)
			frag = match.group(2)
			return buildReleaseMessageWithType(item, 'A Different World Scenery View From the Tower', vol, chp, frag=frag, postfix=postfix)

	return False