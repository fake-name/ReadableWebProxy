def extractLightNovelsWorld(item):
	"""
	Light Novels World
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	
	# This comes first, because it occationally includes non-numbered chapters.
	if 'Tsuki ga Michibiku Isekai Douchuu (POV)' in item['tags']:
		if not postfix and '-' in item['title']:
			postfix = item['title'].split("-")[-1].strip()
		return buildReleaseMessageWithType(item, 'Tsuki ga Michibiku Isekai Douchuur', vol, chp, frag=frag, postfix=postfix)
	
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if 'Announcements' in item['tags']:
		return None
		
	if 'Amaku Yasashii Sekai de Ikiru ni wa' in item['tags']:
		return buildReleaseMessageWithType(item, 'Amaku Yasashii Sekai de Ikiru ni wa', vol, chp, frag=frag, postfix=postfix)
	if 'Omae Mitai na Hiroin ga Ite Tamaruka!' in item['tags']:
		return buildReleaseMessageWithType(item, 'Omae Mitai na Hiroin ga Ite Tamaruka!', vol, chp, frag=frag, postfix=postfix)
	if 'the nine godheads' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Nine Godheads', vol, chp, frag=frag, postfix=postfix)
	if 'World Seed' in item['tags']:
		return buildReleaseMessageWithType(item, 'World Seed', vol, chp, frag=frag, postfix=postfix)
	if 'Asura' in item['tags']:
		return buildReleaseMessageWithType(item, 'Asura', vol, chp, frag=frag, postfix=postfix)
	if 'Infinity Armament' in item['tags']:
		return buildReleaseMessageWithType(item, 'Infinity Armament', vol, chp, frag=frag, postfix=postfix)
	if 'Peerless Demonic Lord' in item['tags']:
		return buildReleaseMessageWithType(item, 'Peerless Demonic Lord', vol, chp, frag=frag, postfix=postfix)
	if 'The Throne Under the Starry Sky' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Throne Under the Starry Sky', vol, chp, frag=frag, postfix=postfix)
	if 'Twin Sword' in item['tags']:
		return buildReleaseMessageWithType(item, 'Twin Sword', vol, chp, frag=frag, postfix=postfix)
	if 'Sayonara Ryuusei Konnichiwa Jinsei' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sayonara Ryuusei Konnichiwa Jinsei', vol, chp, frag=frag, postfix=postfix)
	if 'Online Game: Evil Dragon Against The Heaven' in item['tags']:
		return buildReleaseMessageWithType(item, 'Online Game: Evil Dragon Against The Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'Hakushaku Reijo ha Chito Tensei Mono' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hakushaku Reijo ha Chito Tensei Mono', vol, chp, frag=frag, postfix=postfix)
	if 'Ore to Kawazu-san no Isekai Houriki' in item['tags'] or 'Ore to Kawazu-san no Isekai Hourouki' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore to Kawazu-san no Isekai Houriki', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Blood Warrior' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dragon Blood Warrior', vol, chp, frag=frag, postfix=postfix)
	if 'Evil-like Duke Household' in item['tags']:
		return buildReleaseMessageWithType(item, 'Evil-like Duke Household', vol, chp, frag=frag, postfix=postfix)
	if 'Great Dao Commander' in item['tags']:
		return buildReleaseMessageWithType(item, 'Great Dao Commander', vol, chp, frag=frag, postfix=postfix)
	if 'It’s Impossible that My Evil Overlord is So Cute' in item['tags']:
		return buildReleaseMessageWithType(item, 'It’s Impossible that My Evil Overlord is So Cute', vol, chp, frag=frag, postfix=postfix)
	if 'I’m OP, but I Began an Inn' in item['tags']:
		return buildReleaseMessageWithType(item, 'I’m OP, but I Began an Inn', vol, chp, frag=frag, postfix=postfix)
	if 'The Lame Daoist Priest' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Lame Daoist Priest', vol, chp, frag=frag, postfix=postfix)
	if 'The Last Apostle' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Last Apostle', vol, chp, frag=frag, postfix=postfix)
	if 'Isekai Teni Jobumasuta e no Michi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai Teni Jobumasuta e no Michi', vol, chp, frag=frag, postfix=postfix)
	if 'Against the Fate' in item['tags']:
		return buildReleaseMessageWithType(item, 'Against the Fate', vol, chp, frag=frag, postfix=postfix)
	if 'Hone no aru Yatsu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hone no aru Yatsu', vol, chp, frag=frag, postfix=postfix)
	if 'LV999 Villager' in item['tags']:
		return buildReleaseMessageWithType(item, 'LV999 Villager', vol, chp, frag=frag, postfix=postfix)
	if "Immortal's Farmland" in item['tags']:
		return buildReleaseMessageWithType(item, "Immortal's Farmland", vol, chp, frag=frag, postfix=postfix)
	if 'Returning from the Immortal World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Returning from the Immortal World', vol, chp, frag=frag, postfix=postfix)
	if 'Starchild Escapes Arranged Marriage' in item['tags']:
		return buildReleaseMessageWithType(item, 'Starchild Escapes Arranged Marriage', vol, chp, frag=frag, postfix=postfix)
	if '9 Coffins of the Immortals' in item['tags']:
		return buildReleaseMessageWithType(item, '9 Coffins of the Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Fantastic Creatures’ Travelogue' in item['tags']:
		return buildReleaseMessageWithType(item, 'Fantastic Creatures’ Travelogue', vol, chp, frag=frag, postfix=postfix)
	if "Hell's Cinema" in item['tags']:
		return buildReleaseMessageWithType(item, "Hell's Cinema", vol, chp, frag=frag, postfix=postfix)
	if 'The Great Conqueror' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Great Conqueror', vol, chp, frag=frag, postfix=postfix)
	if 'Almighty Student' in item['tags']:
		return buildReleaseMessageWithType(item, 'Almighty Student', vol, chp, frag=frag, postfix=postfix)
	if 'Godly Student' in item['tags']:
		return buildReleaseMessageWithType(item, 'Godly Student', vol, chp, frag=frag, postfix=postfix)
	if 'Legend of the Cultivation God' in item['tags']:
		return buildReleaseMessageWithType(item, 'Legend of the Cultivation God', vol, chp, frag=frag, postfix=postfix)
	if 'Supreme Arrow God' in item['tags']:
		return buildReleaseMessageWithType(item, 'Supreme Arrow God', vol, chp, frag=frag, postfix=postfix)
	if 'Blade Online' in item['tags']:
		return buildReleaseMessageWithType(item, 'Blade Online', vol, chp, frag=frag, postfix=postfix)
	if 'The Crimson Dragon' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Crimson Dragon', vol, chp, frag=frag, postfix=postfix)
	if 'Sky Prince' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sky Prince', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Aenthar' in item['tags']:
		return buildReleaseMessageWithType(item, 'Aenthar', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'How to Survive a Summoning 101' in item['tags']:
		return buildReleaseMessageWithType(item, 'How to Survive a Summoning 101', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False