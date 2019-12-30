def extractRedLanternArchives(item):
	"""
	# 'Red Lantern Archives'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if 'Synopsis - Summaries' in item['tags']:
		return None
		
	if 'Outaishihi ni Nante Naritakunai!!' in item['tags']:
		return buildReleaseMessageWithType(item, 'Outaishihi ni Nante Naritakunai!!', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		# Geeeez, long enough title much?
		('『Shirayukihime to 7 Nin no Koibito』to iu 18 kin Otomege Heroin ni Tenseishiteshimatta Ore ga Zenryoku de Oujitachi kara Nigeru Hanashi',       
			'『Shirayukihime to 7 Nin no Koibito』to iu 18 kin Otomege Heroin ni Tenseishiteshimatta Ore ga Zenryoku de Oujitachi kara Nigeru Hanashi', 'translated'),
		('Doro Doro Obake Ouji-sama',                                             'Doro Doro Obake Ouji-sama',                                       'translated'),
		('Isekai Trip no Wakiyaku datta Ken',                                     'Isekai Trip no Wakiyaku datta Ken',                               'translated'),
		('Outaishihi ni Nante Naritakunai!!',                                     'Outaishihi ni Nante Naritakunai!!',                               'translated'),
		('Meshitaki Onna ni Yakuza no Ai wa Omosugiru',                           'Meshitaki Onna ni Yakuza no Ai wa Omosugiru',                     'translated'),
		('Eroge Reincarnation　　～Please don’t collect Onee-chan’s CGs～',       'Eroge Reincarnation　　～Please don’t collect Onee-chan’s CGs～', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		
		
	return False