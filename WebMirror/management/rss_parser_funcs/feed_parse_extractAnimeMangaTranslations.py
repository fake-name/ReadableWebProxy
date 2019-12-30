def extractAnimeMangaTranslations(item):
	"""
	Anime, manga, translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	bad = ['Read Online', 
			'Download', 
			'comic', 
			'Anime', 
			'Manga', 
			'Robotech', 
			'Alpen Rose', 
			'Watch Online',
			'Generation Tank',
			'Noboru Miyama',
			'Godo',
			]
	if any([(tmp in item['tags']) for tmp in bad]):
		return None
	if '[Chang Sheng] BABY' in item['title']:
		return None
	if '[RAW]' in item['title']:
		return None
		
		
		
	return False