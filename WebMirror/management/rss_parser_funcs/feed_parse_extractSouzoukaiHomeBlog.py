def extractSouzoukaiHomeBlog(item):
	'''
	Parser for 'souzoukai.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('nidome murabito',                    'Nidome no Jinsei wa Zettai, Shiawase ni! ~Murabito ni Tensei shitan dakedo, Kondo wa Hitonami no Shiawase ga Hoshii! Demo, Dekiru no?~',                      'translated'),
		('ruri to yuri to hime to majo',       'Ruri to Yuri to Hime to Majo',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('double check', 'Double Check',                'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False