def extractTranslatinotakuCf(item):
	'''
	Parser for 'translatinotaku.cf'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Hokage Ryos Path',                      'Hokage: Ryo\'s Path',                      'translated'),
		('The Strongest Hokage',                  'The Strongest Hokage',                     'translated'),
		('God of Soul System',                    'God Of Soul System',                       'translated'),
		('Harry Potter and the Secret Treasures', 'Harry Potter and the Secret Treasures',    'translated'),
		('The King of The Worlds',                'The King of The Worlds',                   'translated'),
		('One Piece: The Soul Purchasing Pirate', 'One Piece: The Soul Purchasing Pirate',    'translated'),
		('Reincarnation Paradise',                'Reincarnation Paradise',                   'translated'),
		('My Inseparable House Guests',           'My Inseparable House Guests',                          'translated'),
		('Heavenly Farmer',                       'Heavenly Farmer',                                      'translated'),
		('Super Card System',                     'Super Card System',                                    'translated'),
		('long live the hokage',                  'long live the hokage',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('G.O.S.S Chapter',  'God Of Soul System',                       'translated'),
		('T.S.H Chapter',    'The Strongest Hokage',                     'translated'),
		('H.R.P Chapter ',   'Hokage: Ryo\'s Path',                      'translated'),
		('F.S Chapter ',     'Fantasy System',                           'translated'),
		('H.P.S.T Chapter ', 'Harry Potter and the Secret Treasures',    'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False