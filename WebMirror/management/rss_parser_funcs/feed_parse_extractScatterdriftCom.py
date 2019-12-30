def extractScatterdriftCom(item):
	'''
	Parser for 'scatterdrift.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Legend of the Great Saint',       'Legend of the Great Saint',                      'translated'),
		('My Wife Is A Princess',           'My Wife Is A Princess',                      'translated'), 
		('Kidnapping All Mankind',          'Kidnapping All Mankind',                      'translated'), 
		('Destroyer of Ice and Fire',       'Destroyer of Ice and Fire',                   'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False