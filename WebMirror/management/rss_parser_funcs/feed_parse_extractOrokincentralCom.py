def extractOrokincentralCom(item):
	'''
	Parser for 'orokincentral.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('demon king executive',       'As The Hero’s Mother, I Became An Executive Of The Demon King’s Army',                      'translated'),
		('deported for innocent charges',       'Former Operations Chief Exiled For Innocent Charges Becomes The Strongest Adventurer',                      'translated'),
		('northwest gas station',       'I Run A Gas Station In The Northwest',                      'translated'),
		('after rebirth, he married his childhood sweetheart',       'after rebirth, he married his childhood sweetheart',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False