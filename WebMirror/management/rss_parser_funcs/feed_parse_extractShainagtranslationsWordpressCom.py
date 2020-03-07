def extractShainagtranslationsWordpressCom(item):
	'''
	Parser for 'shainagtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('The Lady’s Sickly Husband Ch.',      'The Lady\'s Sickly Husband',              'translated'),
			('Rebirth of the Tyrant’s Pet Ch.',    'Rebirth of the Tyrant\'s Pet',            'translated'),
			('The Frog Prince and the Witch Ch.',  'The Frog Prince and the Witch',           'translated'),
			('MLVF Ch.',                           'The Male Lead’s Villainess Fiancée',      'translated'),
			('RotFK Ch. ',                         'Return of the Female Knight',             'translated'),
			('ATP Ch.',                            'Avoid the Protagonist!',                  'translated'),
			('MLSW Ch.',                           'The Male Lead’s Substitute Wife',         'translated'),
			('IDATIAC Ch. ',                       'I Died And Turned Into A Cat',            'translated'),
			('TCVCF Ch.',                          'The CEO’s Villainess Childhood Friend',   'translated'),
			('TTID Ch.',                           'Trapped in a Typical Idol Drama',         'translated'),
			('HSAG Ch.',                           'Heroine Saves A Gentleman',               'translated'),
			('INYFL Ch.',                          'I\'m Not Your Female Lead',               'translated'),
			('DLVM Ch.',                           'Daily Life of a Villain\'s Mother',       'translated'),
			('Master of Dungeon',                  'Master of Dungeon',                       'oel'),
		]
	
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	return False