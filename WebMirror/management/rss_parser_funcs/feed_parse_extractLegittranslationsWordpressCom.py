def extractLegittranslationsWordpressCom(item):
	'''
	Parser for 'legittranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	
	titlemap = [
		('TDS V',                         'The Dungeon Seeker',      'translated'),
		('The Dungeon Seeker – Chapter',  'The Dungeon Seeker',      'translated'),
		('The Dungeon Seeker – Volume ',  'The Dungeon Seeker',      'translated'),
	]

	if item['tags'] == ['Okategoriserade']:   # I'm pretty sure this means "Uncategorized"
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False