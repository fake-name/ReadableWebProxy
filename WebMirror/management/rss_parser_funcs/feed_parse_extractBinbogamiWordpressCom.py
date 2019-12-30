def extractBinbogamiWordpressCom(item):
	'''
	Parser for 'binbogami.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Hazure Skill',       'Hazure Skill ‘Mapping’ wo Te ni Shita Ore wa, Saikyou Party to Tomo ni Dungeon ni Idomu',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False