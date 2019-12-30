def extractHoldX(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('Shoya Kara Hajimeru Ai Aru Seikatsu',                      'Shoya Kara Hajimeru Ai Aru Seikatsu',                      'translated'),
		('Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou',            'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou',            'translated'),
		('Riaru de Reberu Age Shitara Hobo Chītona Jinsei ni Natta', 'Riaru de Reberu Age Shitara Hobo Chītona Jinsei ni Natta', 'translated'),
		('Erogacha',                                                 'Erogacha',                                                 'translated'),
		('Ore no Sekai no Kouryakubon',                              'Ore no Sekai no Kouryakubon',                              'translated'),
		('Takarakuji de 40 oku Atatta Ndakedo i Sekai ni Ijū Suru',  'Takarakuji de 40 oku Atatta Ndakedo i Sekai ni Ijū Suru',  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou',            'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou',            'translated'),
		('Ore no Sekai no Kouryakubon',                              'Ore no Sekai no Kouryakubon',                              'translated'),
		('Erogacha',                                                 'Erogacha',                                                 'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False