def extractTheUndyingCultivator(item):
	"""

	"""
	volstr = str(item['tags']).lower().replace('arc ', 'volume ')
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(volstr + item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	extract = re.search('\\W(\\d+)\\.(\\d+)\\W', item['title'])
	if extract:
		chp = float(extract.group(1))
		frag = float(extract.group(2))
	if 'The Undying Cultivator' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Undying Cultivator', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Undying Prince' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Undying Prince', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False