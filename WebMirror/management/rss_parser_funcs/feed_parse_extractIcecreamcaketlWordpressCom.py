def extractIcecreamcaketlWordpressCom(item):
	'''
	Parser for 'icecreamcaketl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('JikuuMahou',       'Jikuu Mahou de Isekai to Chikyuu wo Ittarikitari',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False