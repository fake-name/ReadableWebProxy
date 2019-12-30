def extractNoodletownTranslated(item):
	"""
	# 'Noodletown Translated'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	titlemap = [
		('[HTK] ',                      'Hail The King',                   'translated'),
		('[AOTDD] ',                    'Ace of the Dragon Division',      'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False