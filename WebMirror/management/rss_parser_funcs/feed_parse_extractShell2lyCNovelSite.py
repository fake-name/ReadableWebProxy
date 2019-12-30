def extractShell2lyCNovelSite(item):
	"""
	# 'Shell2ly C-Novel Site'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	fragfound = re.search('\\((\\d+)\\)', item['title'])
	if not frag and fragfound:
		frag = int(fragfound.group(1))
	if 'MMSTEM' in item['tags']:
		return buildReleaseMessageWithType(item, 'Madam, Master Said to Eat Meal', vol, chp, frag=frag, postfix=postfix)
	return False
