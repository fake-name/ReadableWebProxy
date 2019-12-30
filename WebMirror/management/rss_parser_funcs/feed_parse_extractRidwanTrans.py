def extractRidwanTrans(item):
	"""
	# 'RidwanTrans'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Isekai Meikyuu no Saishinbu wo Mezasou' in item['title']:
		extract = re.search('Chapter (\\d+)\\-(\\d+)', item['title'], re.IGNORECASE)
		if extract and not frag:
			chp = int(extract.group(1))
			frag = int(extract.group(2))
		return buildReleaseMessageWithType(item, 'Isekai Meikyuu no Saishinbu wo Mezasou', vol, chp, frag=frag, postfix=postfix)
	return False
