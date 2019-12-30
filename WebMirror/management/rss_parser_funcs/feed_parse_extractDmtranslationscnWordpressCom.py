def extractDmtranslationscnWordpressCom(item):
	'''
	Parser for 'dmtranslationscn.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	tagmap = [
		('TSLDB',       'The Strongest Legend of Dragon Ball',                      'translated'), 
		('OPTS',        'One Piece Talent System',                                  'translated'), 
		('GGS',         'Galactic Garbage Station',                                 'translated'), 
		('HOM',         'Heroes of Marvel',                                         'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] != ['Uncategorized']:
		return False
		
		
	titlemap = [
		('Time Traveler V',  'Time Traveler',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False