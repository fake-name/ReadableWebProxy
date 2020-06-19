def extractGakuseitranslationsWordpressCom(item):
	'''
	Parser for 'gakuseitranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PGT',       'Every Morning the Most Popular Girl at School Sits Next to Me on the Train',    'translated'),
		('Monrabu',   'Monku no Tsukeyou ga Nai Rabukome',                                             'translated'),
		('Kou2TL',    'The Results From When I Time Leaped to My Second Year of High School and Confessed to the Teacher I Liked at the Time',                                             'translated'),
		('wggc',      'After Coincidentally Saving the New Transfer Student’s Little Sister, We Gradually Grew Closer',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False