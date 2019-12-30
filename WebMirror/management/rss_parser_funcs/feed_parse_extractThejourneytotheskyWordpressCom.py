def extractThejourneytotheskyWordpressCom(item):
	'''
	Parser for 'thejourneytothesky.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Doro Doro', 'Doro Doro Obake Ouji-sama', 'translated')
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if item['tags'] != ['Uncategorized']:
		return False

	titlemap = [
		('[IRM2TM7H]',                      'In Regards to My 2nd Trip and My 7 Husbands',                         'translated'), 
		('Doro Doro Obake Ouji-sama',       'Doro Doro Obake Ouji-sama',                                           'translated'), 
		('Watashi wa Teki ni Narimasen! ',  'Watashi wa Teki ni Narimasen! ',                                      'translated'), 
		('[Arasaa]',                        'I am the Newly Born Woman of Around Thirty',                          'translated'), 
		('The Duke’s daughter ch',          'The Duke\'s Daughter Is the Knight Captain\'s (62) Young Wife',       'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False