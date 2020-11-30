def extractKinokuraWordpressCom(item):
	'''
	Parser for 'kinokura.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('masho no otoko wo mezashimasu',                'masho no otoko wo mezashimasu',                               'translated'),
		('yumemiru danshi wa genjitsushugisha',          'yumemiru danshi wa genjitsushugisha',                         'translated'),
		('naguri tamer no isekai seikatsu',              'naguri tamer no isekai seikatsu',                             'translated'),
		('isekai demo bunan ni ikitai shoukougun',       'isekai demo bunan ni ikitai shoukougun',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False