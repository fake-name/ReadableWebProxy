def extractLandofLightNovels(item):
	"""
	Land of Light Novels
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('C3'):
		return buildReleaseMessageWithType(item, 'Cube x Cursed x Curious', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Chrome Shelled Regios'):
		return buildReleaseMessageWithType(item, 'Chrome Shelled Regios', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Utsuro no Hako to Zero no Maria'):
		return buildReleaseMessageWithType(item, 'Utsuro no Hako to Zero no Maria', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Seirei Tsukai no Blade Dance'):
		return buildReleaseMessageWithType(item, 'Seirei Tsukai no Blade Dance', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Baka to test'):
		return buildReleaseMessageWithType(item, 'Baka to Test', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Tokyo Ravens'):
		return buildReleaseMessageWithType(item, 'Tokyo Ravens', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('The Zashiki Warashi of Intellectual Village'):
		return buildReleaseMessageWithType(item, 'The Zashiki Warashi of Intellectual Village', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Overlord'):
		return buildReleaseMessageWithType(item, 'Overlord', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Mahouka Koukou no Rettousei'):
		return buildReleaseMessageWithType(item, 'Mahouka Koukou no Rettousei', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('To aru New Testament'):
		return buildReleaseMessageWithType(item, 'To Aru Majutsu no Index: New Testament', vol, chp, frag=frag, postfix=postfix)
	return False
