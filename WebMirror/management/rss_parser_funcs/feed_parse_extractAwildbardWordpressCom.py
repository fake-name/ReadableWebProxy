def extractAwildbardWordpressCom(item):
	'''
	Parser for 'awildbard.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Garudeina translations',       'Garudeina',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Garudeina ',                                  'Garudeina',                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if item['title'].lower().startswith(titlecomponent.lower()):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False