def extractInsaneTranslations(item):
	"""
	Parser for 'Insane Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('AnBM',       'Akugyaku No Black Maria', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	

	titlemap = [
		('ABM',                                       'Akugyaku no Black Maria',                                                'translated'),
		('Akugyaku no Black Maria',                   'Akugyaku no Black Maria',                                                'translated'),
		('MLW',                                       'While killing slimes for 300 years, I became the MAX level unknowingly', 'translated'),
		('MAX level witch',                           'While killing slimes for 300 years, I became the MAX level unknowingly', 'translated'),
		('MAX lvl witch',                             'While killing slimes for 300 years, I became the MAX level unknowingly', 'translated'),
		('The Life of Demon Empress Siamara Chapter', 'The Life of Demon Empress Siamara Chapter',                              'oel'),
		('The Beast',                                 'The Beast',                                                              'oel'),
	]

	for titlecomponent, name, tl_type in titlemap: 
		if item['title'].lower().startswith(titlecomponent.lower()):
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	
	# if item['title'].startswith(""):
	# 	return buildReleaseMessageWithType(item, 'Akugyaku no Black Maria', vol, chp, frag=frag, postfix=postfix)
		
	
		
	return False