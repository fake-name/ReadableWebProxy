def extractMsvijayaBlogspotCom(item):
	'''
	Parser for 'msvijaya.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Entertainment Food Service Novel',                   'Entertainment Food Service',                                   'translated'),
		('He\'s Not A Non Entertainment Circle Novel',         'He\'s Not A Non Entertainment Circle',                         'translated'),
		('His Son Has A Richest Billionaires Dad Novel',       'His Son Has A Richest Billionaires Dad',                       'translated'),
		('Today The Manager Is Also Very Kind Novel',          'Today The Manager Is Also Very Kind',                          'translated'),
		('There Is Chef Yu In The Entertainment Circle Novel', 'There Is Chef Yu In The Entertainment Circle',                 'translated'),
		('Canary [Main Attack] Novel',                         'Canary [Main Attack]',                                         'translated'),
		('cannon fodder is always lucky e novel',              'cannon fodder is always lucky e',                              'translated'),
		('Father and Son Novel',                               'Father and Son',                                               'translated'),
		('Florist Little Boss Novel',                          'Florist Little Boss',                                          'translated'),
		('King of Classical Music Novel',                      'King of Classical Music',                                      'translated'),
		('Lion King\'s Adopted Son Novel',                     'Lion King\'s Adopted Son Novel',                               'translated'),
		('He Is Not A Non Entertainment Circle Novel',         'He Is Not A Non Entertainment Circle Novel',                   'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False