def extractAerialrainCom(item):
	'''
	Parser for 'aerialrain.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('mwfv',                               'my whole family are villains',                      'translated'),
		('my whole family are villains',       'my whole family are villains',                      'translated'),
		('gnu',                                'greetings, ninth uncle',                      'translated'),
		('greetings ninth uncle',              'greetings, ninth uncle',                      'translated'),
		('greetings, ninth uncle',             'greetings, ninth uncle',                      'translated'),
		('thdp',                               'the healer demands payment',                      'translated'),
		('the healer demands payment',         'the healer demands payment',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False