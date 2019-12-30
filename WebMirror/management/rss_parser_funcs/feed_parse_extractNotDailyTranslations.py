def extractNotDailyTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Zombie Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Bloodshot One-Eyed Zombie Emperor', vol, chp, frag=frag, postfix=postfix)
	if "Stealing Hero's Lovers" in item['tags']:
		return buildReleaseMessageWithType(item, "Stealing Hero's Lovers", vol, chp, frag=frag, postfix=postfix)
	if 'Nidome no Yuusha' in item['tags']:
		return buildReleaseMessageWithType(item, 'Nidome no Yuusha wa Fukushuu no Michi wo Warai Ayumu. ~Maou yo, Sekai no Hanbun wo Yaru Kara Ore to Fukushuu wo Shiyou~', vol, chp,
		    frag=frag, postfix=postfix)
	return False
