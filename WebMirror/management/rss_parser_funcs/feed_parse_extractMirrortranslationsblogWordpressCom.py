def extractMirrortranslationsblogWordpressCom(item):
	'''
	Parser for 'mirrortranslationsblog.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if 'inktober' in item['tags']:
		return None
	if 'Inktober' in item['title']:
		return None
	if 'art' in item['tags']:
		return None
	
	tagmap = [
		('White Lotus',              'White Lotus',                                               'translated'), 
		('Heaven\'s Blessing',       'Heaven\'s Blessing',                                        'translated'), 
		('ROLYA',                    'Reborn Only to Love You Again',                             'translated'), 
		('DMBHWA',                   'Doctor, My Bottom Half is Wet Again',                       'translated'), 
		('HE',                       'Heaven’s Will',                                             'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Heaven’s Will',               'Heaven’s Will',                   'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False