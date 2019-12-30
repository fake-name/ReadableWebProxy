def extractThisantjustwannasleepWordpressCom(item):
	'''
	Parser for 'thisantjustwannasleep.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Every World Seems Not Quite Right',        'Every World Seems Not Quite Right',                       'translated'),
		('Killing The Same Person Every Time',       'Killing The Same Person Every Time',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Every World Seems Not Quite Right ',        'Every World Seems Not Quite Right',                       'translated'),
		('EWSNQR',                                    'Every World Seems Not Quite Right',                       'translated'),
		('KtSPET',                                    'Killing The Same Person Every Time',                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False