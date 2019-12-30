def extractBakaPervert(item):
	"""
	# 'Baka Pervert'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'fanfic' in item['title'].lower():
		return None

	if 'antihero' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Ultimate Antihero', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('hxh'):
		return buildReleaseMessageWithType(item, 'Hybrid x Heart Magis Academy Ataraxia', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('magika vol'):
		return buildReleaseMessageWithType(item, 'Magika No Kenshi To Shoukan Maou', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('arifureta chapter') and 'finished' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('arifureta '):
		return buildReleaseMessageWithType(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('bahamut ') and 'finished' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Saijaku Muhai no Bahamut', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('seigensou ') and 'finished' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Seirei Gensouki', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('sevens ') and 'finished' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Sevens', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('campiones ') and 'finished' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Campione', vol, chp, frag=frag, postfix=postfix)
		
	return False