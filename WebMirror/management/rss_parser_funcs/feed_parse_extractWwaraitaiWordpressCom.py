def extractWwaraitaiWordpressCom(item):
	'''
	Parser for 'wwaraitai.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('i don\'t care',           'I Don’t Care, So Let Me Go Home!',                      'translated'),
		('caretaker prince',        'I Was Reincarnated as a Villainess, but My Fiancé (Main Hero) is Taking Care of Me?!',                      'translated'),
		('i\'m still stupid',       'I Reincarnated as a Villainess in an Otome Game, but I’m Still Stupid Inside',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Given That I’ve Become a Villainess, I’d Like to Live Freely',  'Given That I\'ve Become a Villainess, I’d Like to Live Freely',      'translated'),
		('Master of Dungeon',                                             'Master of Dungeon',                                                  'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False