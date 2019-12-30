def extractKuroTranslation(item):
	"""
	'Kuro Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Second Summon', 'Isekai Shoukan wa Nidome Desu',                   'translated'),
		('rebirth',       'ReBirth From The Upper World To The Lower World', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False