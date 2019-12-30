def extractWizThiefsNovels(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	titlemap = [
		('My immortality It’s in a Death game',        "My immortality It's in a Death game",            'translated'),
		('Thanks to a different world reincarnation',  'Thanks to a different world reincarnation',      'translated'),
		('Grave “Z”',                                  'Grave "Z"',                                      'translated'),
		('Transferring To An All Magical Boy School',  'Transferring To An All Magical Boy School',      'translated'),
		('T.A.M.B.S. ',                                'Transferring To An All Magical Boy School',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False