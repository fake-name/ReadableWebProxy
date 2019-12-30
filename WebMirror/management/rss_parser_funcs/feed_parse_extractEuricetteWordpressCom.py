def extractEuricetteWordpressCom(item):
	'''
	Parser for 'euricette.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Greatest Alchemist',            'Someday Will I Be The Greatest Alchemist?',                                                                                                                                           'translated'),
		('The Elf is a Freeloader',       'The Elf is a Freeloader',                                                                                                                                                             'translated'),
		('Stepmother',                    'I Obtained a Stepmother. I Obtained a Little Brother. It Appears That Little Brother Is Not Father\'s Child, but a Scum King\'s Child, However, Don\'t Mind It Please ( ´_ゝ`)',      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False