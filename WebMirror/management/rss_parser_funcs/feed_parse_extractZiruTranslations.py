def extractZiruTranslations(item):
	"""
	# Ziru's Musings | Translations~

	"""
	if 'español' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Suterareta Yuusha no Eiyuutan' in item['tags'] or 'Suterareta Yuusha no Eyuutan' in item['tags'] or 'Suterurareta Yuusha no Eiyuutan' in item['tags']:
		extract = re.search('Suterareta Yuusha no Ei?yuutan \\((\\d+)\\-(.+?)\\)', item['title'])
		if extract:
			vol = int(extract.group(1))
			try:
				chp = int(extract.group(2))
				postfix = ''
			except ValueError:
				chp = None
				postfix = extract.group(2)
			return buildReleaseMessageWithType(item, 'Suterareta Yuusha no Eiyuutan', vol, chp, postfix=postfix)
			
	tagmap = [
		('Demon Sword Maiden',                 'Demon Sword Maiden',             'translated'),
		('No Protection Tonight',              'No Protection Tonight',          'translated'),
		('Inside the Cave of Obscenity',       'Inside the Cave of Obscenity',   'translated'),
		('Dragon Bloodline',                   'Dragon Bloodline',               'translated'),
		('Dragon\'s Bloodline',                'Dragon Bloodline',               'translated'),
		('Lazy Dungeon Master',                'Lazy Dungeon Master',            'translated'),
		('kuro no maou',                       'Kuro no Maou',                   'translated'),
		('Happy Peach',                        'Happy Peach',                    'translated'),
		("The Guild's Cheat Receptionist",     "The Guild's Cheat Receptionist", 'translated'),
		('Suterareta Yuusha no Eiyuutan',      'Suterareta Yuusha no Eiyuutan',  'translated'),
		('The Magus of Genesis',               'The Magus of Genesis',           'translated'),
		('atelier may',                        'Easygoing Atelier Life ~May and the Fluffy Miniature Garden~',              'translated'),
		('The Forsaken Hero',                  'The Forsaken Hero',              'translated'),
		('The Restart',                        'The Restart',                    'oel'),
	]
	
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Dragon’s Bloodline — Chapter ',      'Dragon Bloodline',               'translated'),
		('Lazy Dungeon Master ',               'Lazy Dungeon Master',            'translated'),
		('Happy Peach ',                       'Happy Peach',                    'translated'),
		("The Guild’s Cheat Receptionist ",    "The Guild's Cheat Receptionist", 'translated'),
		
		# Somehow, this tag is present, but getting missed? Is there whitespace that's getting truncated?
		('Inside the Cave of Obscenity ',                  'Inside the Cave of Obscenity',        'translated'),
	]

	for titlecomponent, name, tl_type in tagmap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


			
	return False