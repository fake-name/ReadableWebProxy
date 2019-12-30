def extractKoreYoriHachidori(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Seiun wo kakeru'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Seiun wo Kakeru', vol, chp, frag=frag, postfix=postfix)
	if 'Ochitekita'.lower() in item['title'].lower() or 'Ochitekita Naga to Majo no Kuni' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ochitekita Naga to Majo no Kuni', vol, chp, frag=frag, postfix=postfix)
	if 'Humans are the Strongest Race' in item['tags']:
		return buildReleaseMessageWithType(item, 'Humans are the Strongest Race ~Starting a Slow Life with an Elf Wife in a Different World~', vol, chp, frag=frag, postfix=postfix)
	return False
