def extractNormalpandaCom(item):
	'''
	Parser for 'normalpanda.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	titlemap = [
		('SFVSG CH.',                'School Flower versatile security guard',      'translated'),
		('PF Ch.',                   'Perfect Feast',                               'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False