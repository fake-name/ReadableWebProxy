def extractMike777ac(item):
	"""
	# Mike777ac

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not postfix and ':' in item['title']:
		postfix = item['title'].split(':')[-1]
	if ('Hardcore OPness' in item['tags'] or 'HCOP' in item['tags']) and (chp or vol):
		return buildReleaseMessageWithType(item, 'Hardcore OP-ness', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
