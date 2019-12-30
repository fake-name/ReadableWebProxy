def extractChineseBLTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Novel: City of Endless Rain',                  'City of Endless Rain',              'translated'),
		('Novel: Cold Sands',                            'Cold Sands',                        'translated'),
		('Novel: The Rental Shop Owner',                 'The Rental Shop Owner',             'translated'),
		('Novel: Till Death Do Us Part',                 'Till Death Do Us Part',             'translated'),
		('Novel: Love Late',                             'Love Late',                         'translated'),
		('Novel: Spring Once More',                      'Spring Once More',                  'translated'),
		('Novel: Brother',                               'Brother',                           'translated'),
		('Novel: Living to Suffer',                      'Living to Suffer',                  'translated'),
		('Novel: How Dare You Attack My Support!',       'How Dare You Attack My Support!',   'translated'),
		('Novel: Going Out of the Way to Love You',      'Going Out of the Way to Love You',  'translated'),
		('novel: the ten years when i loved you so',     'The Ten Years When I Loved You So', 'translated'),
		('Novel: Turning the Corner to Love You',        'Turning the Corner to Love You',    'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False