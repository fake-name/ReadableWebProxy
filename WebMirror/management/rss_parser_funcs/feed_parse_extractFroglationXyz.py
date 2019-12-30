def extractFroglationXyz(item):
	'''
	Parser for 'froglation.xyz'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	bad = [
			'Fukusyu wo Chikatta Shironeko wa Ryuuou no Hiza no ue de Damin wo Musaboru (Manga)',
		]
	
	if any([tmp in item['tags'] for tmp in bad]):
		return None

	tagmap = [
		('Fukusyu wo Chikatta Shironeko wa Ryuuou no Hiza no ue de Damin wo Musaboru',            'Fukusyu wo Chikatta Shironeko wa Ryuuou no Hiza no ue de Damin wo Musaboru',                           'translated'),
		('Fukusyu wo Chikatta Shironeko wa Ryuuou no Hiza no ue de Damin wo Musaboru (WN)',       'Fukusyu wo Chikatta Shironeko wa Ryuuou no Hiza no ue de Damin wo Musaboru (WN)',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False