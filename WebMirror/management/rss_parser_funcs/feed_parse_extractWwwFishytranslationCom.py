def extractWwwFishytranslationCom(item):
	'''
	Parser for 'www.fishytranslation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Op Waifus',                                          'Being Able to Edit Skills in Another World, I Gained OP Waifus',                               'translated'),
		('Rebirth Junior High School',                         'Rebirth Junior High School: The Exceling Top Student Goddess',                                 'translated'),
		('How to Raise a Silver-Haired Loli',                  'How to Raise a Silver-Haired Loli',                                                            'translated'),
		('The Pitiful Me Does Not Need a Dazzling Life',       'The Pitiful Me Does Not Need a Dazzling Life',                                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False