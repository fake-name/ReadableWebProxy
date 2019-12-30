def extractAvaritiakun(item):
	"""
	Avaritia-kun
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Divine protection',  'The divine protection that I got was a power that increase a girl level with semen', 'translated'),
		('Rose',               'Rose in a Yuri Field', 'translated'),
		('Rose and lily field',   'Rose in a Yuri Field', 'translated'),
		('Perfect Sex',           'Perfect Sex', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
		
	return False