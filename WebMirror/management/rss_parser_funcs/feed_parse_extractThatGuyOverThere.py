def extractThatGuyOverThere(item):
	"""
	# That Guy Over There

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'wushenkongjian' in item['tags']:
		return buildReleaseMessageWithType(item, 'Wu Shen Kong Jian', vol, chp, frag=frag)
	match = re.search('^Le Festin de Vampire – Chapter (\\d+)\\-(\\d+)', item['title'])
	if match:
		chp = match.group(1)
		frag = match.group(2)
		return buildReleaseMessageWithType(item, 'Le Festin de Vampire', vol, chp, frag=frag)
	return False
