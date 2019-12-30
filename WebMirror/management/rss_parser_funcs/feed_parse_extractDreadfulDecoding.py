def extractDreadfulDecoding(item):
	"""

	"""
	
	if 'Manga' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	extractVol = re.search('\\[[A-Z]+(\\d+)\\]', item['title'])
	if not vol and extractVol:
		vol = int(extractVol.group(1))
	extractChp = re.search('SECT\\.(\\d+) ', item['title'])
	if chp == 1 and 'SECT.' in item['title'] and extractChp:
		chp = int(extractChp.group(1))
	if 'Gun Gale Online' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sword Art Online Alternative - Gun Gale Online', vol, chp, frag=frag, postfix=postfix)
	if 'RotTS' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sword Art Online Alternative - Rondo of the Transient Sword', vol, chp, frag=frag, postfix=postfix)
	return False