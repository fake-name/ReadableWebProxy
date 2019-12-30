def extractLESYT(item):
	"""
	LESYT
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		 
	
	snames = [
		
			'Chronicles of Primordial Wars',
			'The Silly Alchemist',
			'Swallowing the Heavens',
			'Thunder Martial',
			'The Ocean Flame Palace Host',
			'I am a Bastard',
			'The Samsara Cycle',
			'The Thrilling Sword',
			'Fanatic Martial God',
			'The City\'s Invincible Soldier King',
			'The Supreme Sword',
			'Heavenly Martial Throne',
			'I Sell Tantric Amulets in Thailand',
		]
	
	tlut = {tmp.lower(): tmp for tmp in snames}
	
	    
	tlut['demon god'] = "Demon God"
	
	ltags = [tmp.lower() for tmp in item['tags']]
	for key, value in tlut.items():
		if key in ltags:
			tl_type = 'translated'
			
			return buildReleaseMessageWithType(item, value, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	return False