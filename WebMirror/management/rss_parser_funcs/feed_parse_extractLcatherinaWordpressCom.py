def extractLcatherinaWordpressCom(item):
	'''
	Parser for 'lcatherina.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('BFGAH',                                                                    'Beastly Fēi that Go Against the Heaven: Coerced by the Huáng Shū',                      'translated'),
		('Beastly Fēi that Goes Against the Heaven: Coerced by the Huáng Shū',       'Beastly Fēi that Go Against the Heaven: Coerced by the Huáng Shū',                      'translated'),
		('Pampered Fei Brimming with Cuteness',                                      'Pampered Fei Brimming with Cuteness',                                                   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False