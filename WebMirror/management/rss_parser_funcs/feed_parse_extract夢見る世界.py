def extract夢見る世界(item):
	"""
	Parser for '夢見る世界'
	"""
	
	if 'Otome Games' in item['tags']:
		return None
	if 'Drama CDs' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Miss Appraiser and Gallery Demon',       'Miss Appraiser and Gallery Demon',                      'translated'), 
		('Light Beyond Road\'s End',               'Light Beyond (LN)',                                     'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
			
	return False