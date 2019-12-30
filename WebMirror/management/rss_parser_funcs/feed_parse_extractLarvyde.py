def extractLarvyde(item):
	"""
	# Larvyde Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Preview' in item['tags']:
		return None
	if not postfix and '–' in item['title']:
		postfix = item['title'].split('–')[-1]
	if 'Ore no Osananajimi wa Joshikousei de Yuusha' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore no Osananajimi wa Joshikousei de Yuusha', vol, chp, frag=frag, postfix=postfix)
	if 'Oukoku e Tsuzuku Michi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Oukoku e Tsuzuku Michi', vol, chp, frag=frag, postfix=postfix)
	if 'Takarakuji de 40-oku Atattandakedo' in item['tags']:
		return buildReleaseMessageWithType(item, 'Takarakuji de 40 Oku Atattandakedo Isekai ni Ijuu Suru', vol, chp, frag=frag, postfix=postfix)
	if 'Jaaku Chika Teikoku' in item['tags']:
		return buildReleaseMessageWithType(item, 'Jaaku to Shite Akuratsu Naru Chika Teikoku Monogatari', vol, chp, frag=frag, postfix=postfix)
	if 'Saenai Heroine no Sodatekata' in item['tags']:
		return buildReleaseMessageWithType(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)
	if 'Genjitsushugisha no Oukokukaizouki' in item['tags']:
		return buildReleaseMessageWithType(item, 'Genjitsushugisha no Oukokukaizouki', vol, chp, frag=frag, postfix=postfix)
	if 'Hitokui Dungeon e Youkoso' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hitokui Dungeon e Youkoso', vol, chp, frag=frag, postfix=postfix)
	if 'Chikyuu Tenseisha no Koroshikata' in item['tags']:
		return buildReleaseMessageWithType(item, 'Chikyuu Tenseisha no Koroshikata', vol, chp, frag=frag, postfix=postfix)
	return False
