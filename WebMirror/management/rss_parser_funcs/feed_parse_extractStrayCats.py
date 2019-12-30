def extractStrayCats(item):
	"""
	'StrayCats'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Virtual World: The Legendary Thief',       'Virtual World: The Legendary Thief',                      'translated'), 
		('Hiraheishi wa Kako o Yumemiru',       'Hiraheishi wa Kako o Yumemiru',                      'translated'), 
		('Ore no Isekai Shimai ga Jichou Shinai!',       'Ore no Isekai Shimai ga Jichou Shinai!',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False