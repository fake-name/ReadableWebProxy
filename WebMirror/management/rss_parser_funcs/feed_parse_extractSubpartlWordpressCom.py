def extractSubpartlWordpressCom(item):
	'''
	Parser for 'subpartl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('It Seems Like My Body is Completely Invincible',       'It Seems Like My Body is Completely Invincible',                      'translated'),
		('Magi Craft Meister',       'Magi Craft Meister',                      'translated'),
		('MCM',                      'Magi Craft Meister',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False