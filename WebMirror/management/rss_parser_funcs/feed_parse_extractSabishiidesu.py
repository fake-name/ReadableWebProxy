def extractSabishiidesu(item):
	"""
	Sabishii desu!
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if 'tags' in item['tags']:
		return None
		

	tagmap = [
		('Sono-sha. Nochi ni. . .',                   'Sono-sha. Nochi ni. . .',                   'translated'),
		('Sonomono. Nochi ni.....',                   'Sono-sha. Nochi ni. . .',                   'translated'),
		('Ore Dake Shoki Jobu Ga Maōdatta Ndaga',     'Ore Dake Shoki Jobu Ga Maōdatta Ndaga',     'translated'),
		('VRMMO Summoner Hajimemashita',              'VRMMO Summoner Hajimemashita',              'translated'),
		("My Room Has Become A Dungeon's Rest Area",  "My Room Has Become A Dungeon's Rest Area",  'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False