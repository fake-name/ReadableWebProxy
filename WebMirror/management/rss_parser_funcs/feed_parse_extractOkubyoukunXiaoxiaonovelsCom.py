def extractOkubyoukunXiaoxiaonovelsCom(item):
	'''
	Parser for 'okubyoukun.xiaoxiaonovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	tagmap = [
		('Outstanding Dog',       'Outstanding Dog',                                                  'translated'), 
		('Inaka Life',            'Inaka Life',                                                       'translated'), 
		('otome game',            'Dare ga Otome Geemu Dato Itta!',                                   'translated'), 
		('Four Ikemen',           '4-nin no Ikemen ni Kyuuai sarete Ore wa Namidamedesu Index',       'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False