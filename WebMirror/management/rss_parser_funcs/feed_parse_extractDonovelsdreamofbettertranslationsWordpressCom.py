def extractDonovelsdreamofbettertranslationsWordpressCom(item):
	'''
	Parser for 'donovelsdreamofbettertranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Last Boss Witch',           'The Last Boss Witch Will Keep Her Past Self’s Crush Until Her Dying Day',                                                'translated'),
		('Darkness Villainess',       'I\'m Not a Villainess!! Just Because I Can Control Darkness Doesn\'t Mean I\'m a Bad Person! (LN)',                      'translated'),
		('Villainess vs Zombies',     'Villainess vs Zombies',                                                                                                  'translated'),
		('The Ice’s Yearning',        'The Ice’s Yearning',                                                                                                     'translated'),
		('Ice Queen',                 'The Ice’s Yearning',                                                                                                     'translated'),
		('cinderella',                'Fake Cinderella (WN)',                                                                                                   'translated'),
		('Loiterous',                 'Loiterous',                                                                                                              'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False