def extractOyasumiReads(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'ISEKAIJIN NO TEBIKISHO' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekaijin no Tebikisho', vol, chp, frag=frag, postfix=postfix)
	if 'OTOTSUKAI WA SHI TO ODORU' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ototsukai wa Shi to Odoru', vol, chp, frag=frag, postfix=postfix)
	return False