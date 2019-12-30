def extractStitchietranslatorsWordpressCom(item):
	'''
	Parser for 'stitchietranslators.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the royal\'s cute little wife',       'The Royal\'s Cute Little Wife',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('All The Male Protagonists Have Blackened Chapter ',  'All The Male Leads Have Blackened',      'translated'),
		('All The Male Leads Have Blackened Chapter ',         'All The Male Leads Have Blackened',      'translated'),
		('Tensei Shoujo no Rirekisho',                         'Tensei Shoujo no Rirekisho',             'translated'),
		('The Royal’s Cute Little Wife: Chapter ',             'The Royal\'s Cute Little Wife',          'translated'),
		('Master of Dungeon',                                  'Master of Dungeon',                      'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False