def extractFrozensLazyBlog(item):
	"""
	Frozen's Lazy Blog
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None


	tagmap = [
		('Kuusen Madoushi',           'Kuusen Madoushi',                                           'translated'),
		('Last Embryo',               'Last Embryo',                                               'translated'),
		('Vanquish Overlord',         'Vanquish Overlord',                                         'translated'),
		('Majo no Tabitabi',          'Majo no Tabitabi',                                          'translated'),
		('Okaa-san wa Suki desu ka?', 'Okaa-san wa Suki desu ka?',                                 'translated'),
		('Amagi Brilliant Park',      'Amagi Brilliant Park',                                      'translated'),
		('mondaiji',                  'Mondaiji-tachi ga Isekai kara Kuru Sou Desu yo?',           'translated'),
		('Rakudai Kishi',             'Rakudai Kishi No Eiyuutan',                                 'translated'),
		('Isekai NEET',               'Did You Think Another World Would Motivate A NEET?',        'translated'),
		('Riku and Chise',            'Riku and Chise: The Paperboy and The Princess',             'translated'),
		('Granblue Fantasy',          'Granblue Fantasy',                                          'translated'),
		('Miyamoto Sakura',           'Just A Story About Miyamoto Sakura Being Cute',             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



		
	return False