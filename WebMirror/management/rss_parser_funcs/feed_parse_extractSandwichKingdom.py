def extractSandwichKingdom(item):
	"""
	#'Sandwich Kingdom'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'sougen no okite' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sougen no Okite ~Shii yatsu ga moteru, ii buzoku ni umarekawatta zo~', vol, chp, frag=frag, postfix=postfix)
	if 'Q.Maou-sama A.Mamono' in item['tags']:
		return buildReleaseMessageWithType(item, 'Q. Maou-sama no oshigoto wa? A. Mamono musume e no tanetsuke desu', vol, chp, frag=frag, postfix=postfix)
	if 'kininaru kanojo wo tokoton okashi tsukusu hanshi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kininaru Kanojo wo Totokon Okashi Tsukusu Hanashi', vol, chp, frag=frag, postfix=postfix)
	if 'game sekai tenseishitara' in item['tags']:
		return buildReleaseMessageWithType(item, 'After Reincarnating Into This Game World I Seemed to Have Taken Over the Control of Status', vol, chp, frag=frag, postfix=postfix)
	if 'healing semen' in item['tags']:
		return buildReleaseMessageWithType(item, 'Curing incurable disease with semen', vol, chp, frag=frag, postfix=postfix)
	if 'Kininaru' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ki ni Naru Kanojo wo Tokoton Okashitsukusu Hanashi', vol, chp, frag=frag, postfix=postfix)
	if 'Betrayed Hero' in item['tags']:
		return buildReleaseMessageWithType(item, 'Summoned As a Hero, but I Got Betrayed', vol, chp, frag=frag, postfix=postfix)
	if 'yandere' in item['tags']:
		return buildReleaseMessageWithType(item, 'My older sister fell in love with me and turned into a yandere, it seems', vol, chp, frag=frag, postfix=postfix)
	if 'TGFY' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Girl From Yesterday', vol, chp, frag=frag, postfix=postfix)
	return False