def extractOverlordvolume10BlogspotCom(item):
	'''
	Parser for 'overlordvolume10.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if "manga" in item['title'].lower():
		return None

	if "Overlord" in item['tags']:
		return buildReleaseMessageWithType(item, "Overlord", vol, chp, frag=frag, postfix=postfix)
	
	if item['tags'] == []:
		titlemap = [
			('Overlord Gaiden - Chapter ',  'Overlord Gaiden',      'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	
	return False