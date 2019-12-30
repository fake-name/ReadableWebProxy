def extractWeleTranslations(item):
	"""
	Parser for 'Wele Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	guidmap = [
		('/zhan-xian/zhan-xian-chapter-',                     'Zhanxian',                         'translated'),
		('/sin-city/sin-city-chapter-',                       'Sin City',                         'translated'),
		('/martial-god/martial-god-chapter-',                 'Martial God',                      'translated'),
		('/heaven-awakening/heaven-awakening-chapter-',       'Heaven Awakening Path',            'translated'),
	]

	for tagname, name, tl_type in guidmap:
		if tagname in item['guid']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False