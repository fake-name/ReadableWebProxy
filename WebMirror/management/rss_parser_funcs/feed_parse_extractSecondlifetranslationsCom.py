def extractSecondlifetranslationsCom(item):
	'''
	Parser for 'secondlifetranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('IH',        'Immoral Holidays',                            'translated'),
		('ebpw',      'Everyday, Boss Is Pretending To Be Weak',     'translated'),
		('icd',       'Indulging in Carnal Desire',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False