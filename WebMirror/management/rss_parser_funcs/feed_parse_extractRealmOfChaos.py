def extractRealmOfChaos(item):
	"""
	#'Realm of Chaos'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Myriad of Shades' in item['tags']:
		names = [tmp for tmp in item['tags'] if tmp in ['Celest Ambrosia', 'Kiriko', 'Melanie Ambrosia', 'Shana Bonnet', 'Silvia', 'XCrossJ', 'Ghost']]
		postfix_out = ', '.join(names)
		if postfix:
			postfix_out += ' - ' + postfix
		return buildReleaseMessageWithType(item, 'Myriad of Shades', vol, chp, frag=frag, postfix=postfix_out, tl_type='oel')
	return False
