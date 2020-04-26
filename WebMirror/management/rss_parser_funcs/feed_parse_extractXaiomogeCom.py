def extractXaiomogeCom(item):
	'''
	Parser for 'xaiomoge.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol):
		return None

	if "preview" in item['title'].lower():
		return None



	tagmap = [
		('Mechanical God Emperor',                                           'Mechanical God Emperor',                                                          'translated'),
		('Unfathomable Doomsday',                                            'Unfathomable Doomsday',                                                           'translated'),
		('The Defeated Dragon',                                              'The Defeated Dragon',                                                             'translated'),
		('the ancestor of our sect isn’t acting like an elder',              'the ancestor of our sect isn’t acting like an elder',                             'translated'),
		('cultural invasion in another world',                               'cultural invasion in another world',                                              'translated'),
		('Age of Collapse',                                                  'Age of Collapse',                                                                 'translated'),
		('Loiterous',                                                        'Loiterous',                                                                       'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False