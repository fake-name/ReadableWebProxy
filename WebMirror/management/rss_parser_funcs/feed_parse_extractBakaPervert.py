def extractBakaPervert(item):
	"""
	# 'Baka Pervert'
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	
	ltitle = item['title'].lower()
	if not (chp or vol or frag) or 'preview' in ltitle:
		return None
		
	if 'fanfic' in ltitle:
		return None

	if 'antihero' in ltitle:
		return buildReleaseMessageWithType(item, 'Ultimate Antihero', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('hxh'):
		return buildReleaseMessageWithType(item, 'Hybrid x Heart Magis Academy Ataraxia', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('magika vol'):
		return buildReleaseMessageWithType(item, 'Magika No Kenshi To Shoukan Maou', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('arifureta chapter') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('arifureta '):
		return buildReleaseMessageWithType(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('bahamut ') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Saijaku Muhai no Bahamut', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('seigensou ') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Seirei Gensouki', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('sevens ') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Sevens', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('campiones ') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Campione', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('otomege ') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Otomege Sekai wa Mob ni Kibishii Sekai desu', vol, chp, frag=frag, postfix=postfix)
	if ltitle.startswith('maou gakuen ') and 'finished' in ltitle:
		return buildReleaseMessageWithType(item, 'Maou Gakuen no Hangyakusha ~Jinrui Hatsu no Maou Kouhou, Kenzoku Shoujo to Ouza wo Mezashite Nariagaru~', vol, chp, frag=frag, postfix=postfix)
		

		
	return False