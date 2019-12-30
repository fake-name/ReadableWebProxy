def extractSakutranslationsBlogspotCom(item):
	'''
	Parser for 'sakutranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Hidden Dungeon',       'The Hidden Dungeon Only I Can Enter',   'translated'), 
		('Skill Collector',      'The Skill Collector',                   'translated'), 
		('Instant Death',        'Instant Death',                         'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Instant Death ',     'Instant Death',                            'translated'),
		('Hidden Dungeon ',  'The Hidden Dungeon Only I Can Enter',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if item['title'].lower().startswith(titlecomponent.lower()):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False