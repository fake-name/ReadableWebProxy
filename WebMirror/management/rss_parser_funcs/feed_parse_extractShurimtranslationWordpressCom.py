def extractShurimtranslationWordpressCom(item):
	'''
	Parser for 'shurimtranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if '(manga)' in item['title'].lower():
		return None
		
		
	tagmap = [
		("A Wild Last Boss Appeared",                   "A Wild Last Boss Appeared",                 "translated"),
		("Tensei Shitara Slime Datta Ken",              "Tensei Shitara Slime Datta Ken",            "translated"),
		("Konjiki no Moji Tsukai",                      "Konjiki no Moji Tsukai",                    "translated"),
		("Owarimonogatari",                             "Owarimonogatari",                           "translated"),
		("Monogatari Series",                           "Monogatari Series",                         "translated"),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('A Wild Last Boss Appeared: Chapter',  'A Wild Last Boss Appeared',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	if item['title'].startswith('Owarimonogatari') and 'Completed' in item['title']:
		return buildReleaseMessageWithType(item, "Owarimonogatari", vol, chp, frag=frag, postfix=postfix)
		

	return False