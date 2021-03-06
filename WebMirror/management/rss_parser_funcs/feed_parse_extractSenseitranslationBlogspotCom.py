def extractSenseitranslationBlogspotCom(item):
	'''
	Parser for 'senseitranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('S. B. F. C Chapter ',   'Salvation Began From Cafe',      'translated'),
		('S. B. F. C. Chapter ',  'Salvation Began From Cafe',      'translated'),
		('S.B.F.C Chapter',       'Salvation Began From Cafe',      'translated'),
		('S.B.F.C. Chapter',      'Salvation Began From Cafe',      'translated'),
		('OPJ Chapter ',          'One Punch of Justice',           'translated'),
		('M. F. Chapter ',        'Monster Factory',           'translated'),
		('M. F Chapter ',         'Monster Factory',           'translated'),
		('Master of Dungeon',     'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False