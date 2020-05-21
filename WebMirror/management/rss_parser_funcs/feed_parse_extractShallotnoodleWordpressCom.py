def extractShallotnoodleWordpressCom(item):
	'''
	Parser for 'shallotnoodle.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('surrounded mob wants to quietly withdraw',                    'surrounded mob wants to quietly withdraw',                                   'translated'),
		('live broadcasting raising dragons in the interstellar',       'live broadcasting raising dragons in the interstellar',                      'translated'),
		('straight playboy sub',                                        'straight playboy sub',                                                       'translated'),
		('one and only',                                                'One and Only',                                                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False