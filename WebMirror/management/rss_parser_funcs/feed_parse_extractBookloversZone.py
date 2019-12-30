def extractBookloversZone(item):
	'''
	Parser for 'booklovers.zone'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if 'juliet marillier' in item['tags']:
		return None

	tagmap = [
		('how to escape from an implacable man',       'How to Escape from the Implacable Man',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	return False