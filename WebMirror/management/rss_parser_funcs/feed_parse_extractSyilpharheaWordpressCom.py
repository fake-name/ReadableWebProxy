def extractSyilpharheaWordpressCom(item):
	'''
	Parser for 'syilpharhea.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [ 
		('Banished Healer',        'The Healer Banished From The Party, In Fact, Is The Strongest',                                                    'translated'),
		('Re-summoned Hero',       'Will the Re-Summoned Hero Live as an Ordinary Person',                                                             'translated'),
		('Headless Dullahan',      'I’m a Dullahan, Looking for My Head',                                                                              'translated'),
		('Goddess\'s Suffering',   'I Already Said I Don’t Want to Be Reincarnated, Didn’t I!? ~the Suffering of the Goddess of Reincarnation~',       'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False