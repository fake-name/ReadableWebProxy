def extractWwwStarvearchiveCom(item):
	'''
	Parser for 'www.starvearchive.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Diary of the Truant Death God',      'The Diary of the Truant Death God',         'translated'),
		('The Records of the Human Emperor',       'The Records of the Human Emperor',          'translated'),
		('Library of Heaven\'s Path',              'Library of Heaven\'s Path',                 'translated'),
		('The Adonis Next Door',                   'The Adonis Next Door',                      'translated'),
		('Tian Ying',                              'Shadow of the Sky',                         'translated'),
		('Long Fu',                                'Dragon Talisman',                           'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	urlfrag = [
		('/my-master-has-disconnected-again-chapter-',  'My Master Has Disconnected Again',     'translated'),
		('/library-of-heavens-path-chapter-',           'Library of Heaven\'s Path',            'translated'),

	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False