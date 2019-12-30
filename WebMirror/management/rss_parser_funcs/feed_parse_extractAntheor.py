def extractAntheor(item):
	"""
	Antheor
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Hisshou Dungeon Unei Houhou',     'Hisshou Dungeon Unei Houhou',                                               'translated'),
		('HDUH Annoucement',                'Hisshou Dungeon Unei Houhou',                                               'translated'),
		('KYNE Announcement',               'Kami Sumeragi Yuusha no eiyuutan 《Ryokou Tan》',                           'translated'),
		('WWM Announcement',                'The world is overflowing with monster, I’m taking a liking to this life',   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False