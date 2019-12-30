def extract88TangeatdrinkreadWordpressCom(item):
	'''
	Parser for '88tangeatdrinkread.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Prestigious Family Marriage: Uncle vs Young Wife',                      'Prestigious Family Marriage: Uncle vs Young Wife',                                     'translated'),
		('Remarry, No Way!',                                                      'Remarry, No Way!',                                                                     'translated'),
		('Remarrynoway',                                                          'Remarry, No Way!',                                                                     'translated'),
		('I used to be alone until I meet you',                                   'I Used To Be Alone Until I Meet You',                                                  'translated'),
		('Memoirs of Love',                                                       'Memoirs of Love',                                                                      'translated'),
		('Marry! My Black Horse',                                                 'Marry! My Black Horse',                                                                'translated'),
		('The most pleasant thing to hear',                                       'The Most Pleasant Thing to Hear',                                                      'translated'),
		('Systematic director’s tender love',                                     'Systematic Director\'s Tender Love',                                                   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False