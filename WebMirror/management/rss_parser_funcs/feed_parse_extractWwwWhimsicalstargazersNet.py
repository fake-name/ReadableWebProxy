def extractWwwWhimsicalstargazersNet(item):
	'''
	Parser for 'www.whimsicalstargazers.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Reborn Little Girl Won\'t Give Up',              'The Reborn Little Girl Won\'t Give Up',                                     'translated'),
		('Drop!!　～A Tale of the Fragrance Princess～',       'Drop!!　～A Tale of the Fragrance Princess～',                              'translated'),
		('The Saint\'s Magic Power is Omnipotent',             'The Saint\'s Magic Power is Omnipotent',                                    'translated'),
		('princess bibliophile',                               'princess bibliophile',                                                      'translated'),
		('a rose dedicated to you',                            'a rose dedicated to you',                                                   'translated'),
		('slimes can dream too',                               'slimes can dream too',                                                      'translated'),
		('i was reincarnated and now i&#039;m a maid',         'i was reincarnated and now i\'m a maid',                                    'translated'),
		('i was reincarnated and now i\'m a maid',             'i was reincarnated and now i\'m a maid',                                    'translated'),
		('blue monster\'s shell',                              'The Blue Monster\'s Shell',                                                 'translated'),
		('Eliza',                                              'I Reincarnated as a Noble Villainess But Why Did It Turn Out Like This?',   'translated'),
		('Just the Two of Us in this Vast World',              'Just the Two of Us in this Vast World',                                     'translated'),
		('Kill The Dragon',                                    'Kill The Dragon',                                                           'translated'),
		('east road quest',                                    'east road quest',                                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False