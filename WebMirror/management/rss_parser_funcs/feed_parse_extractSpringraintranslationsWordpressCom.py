def extractSpringraintranslationsWordpressCom(item):
	'''
	Parser for 'springraintranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('mary sue does not stick to the plot',             'mary sue does not stick to the plot',          'translated'),
		('scheming villainess\'s counterattack',            'scheming villainess\'s counterattack',         'translated'),
		('Princess and the General',                        'Princess and the General',                     'translated'),
		('Shen Yi Di Nu',                                   'Shen Yi Di Nu',                                'translated'),
		('Epoch of the Dragon',                             'X – Epoch of the Dragon',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False