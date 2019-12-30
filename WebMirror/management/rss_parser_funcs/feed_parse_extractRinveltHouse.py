def extractRinveltHouse(item):
	"""
	Rinvelt House
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Isekai Gakkyuu',       'Chou! Isekai Gakkyuu!!',                      'translated'),
		('Rokujouma',            'Rokujouma no Shinryakusha!?',                      'translated'), 
		('Saratoga',             'Mobile Fortress Saratoga ~Silvery Sword Princess Became My Servant.',                      'translated'), 
		('Dandelion',            'This is the Lively Dandelion House ～Landlord’s and Tenants’ Rent War～',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False