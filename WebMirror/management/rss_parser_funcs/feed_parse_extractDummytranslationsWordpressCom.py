def extractDummytranslationsWordpressCom(item):
	'''
	Parser for 'dummytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the people who\'re supposed to kill me fell for me instead',         'The People Who’re Suppose to Kill Me All Fell for Me Instead',                      'translated'),
		('The people who are supposed to kill me fell for me instead',         'The People Who’re Suppose to Kill Me All Fell for Me Instead',                      'translated'),
		('The People Who’re Suppose to Kill Me All Fell for Me Instead',       'The People Who’re Suppose to Kill Me All Fell for Me Instead',                      'translated'),
		('The target always thinks that I like him',                           'The target always thinks that I like him',                                          'translated'),
		('The little flower god and the emperor',                              'The little flower god and the emperor',                                             'translated'),
		('could you not tease me',                                             'could you not tease me',                                                            'translated'),
		('my nemesis has finally gone bankrupt',                               'my nemesis has finally gone bankrupt',                                              'translated'),
		('fake demon lord',                                                    'fake demon lord',                                                                   'translated'),
		('i have a sickness',                                                  'i have a sickness',                                                                 'translated'),
		('Number One Zombie Wife',                                             'Number One Zombie Wife',                                                            'translated'),
		('The General\'s cat always wants to climb into my bed',               'The General\'s cat always wants to climb into my bed',                              'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False