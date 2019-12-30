def extractYuNSTranslations(item):
	"""
	'yuNS Translations'
	"""
	if "(Manga)" in item['title']:
		return None
		
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		

	titlemap = [
		('Akashic Records of the Bastard Magical Instructor',  'Akashic Records of the Bastard Magical Instructor',      'translated'),
		('Akashic Records of the Bastard Magic Instructor',    'Akashic Records of the Bastard Magical Instructor',      'translated'),
		('Gifting this Wonderful World with Blessings!',       'Gifting this Wonderful World with Blessings!',           'translated'),
		('Gifting this Wonderful Worlds with Explosions!',     'Gifting this Wonderful Worlds with Explosions!',         'translated'),
		('I Shaved. Then I Brought a High School Girl Home',     'I Shaved. Then I Brought a High School Girl Home',         'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		
	return False