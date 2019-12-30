def extractHenoujiTranslation(item):
	"""
	# Henouji Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	numeric_start = False
	try:
		v = int(item['title'].split(' ')[0])
		numeric_start = True
	except ValueError:
		pass
	
	if item['tags'] == ['Web Novel'] and chp and not vol and  numeric_start:
		vol = 3
		return buildReleaseMessageWithType(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)
	if item['tags'] == ['Light Novel'] and chp and not vol and  numeric_start:
		vol = 3
		return buildReleaseMessageWithType(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)
		
	if 'Get Naked' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)
	if 'What Came to Mind During my Third Time in Another World was to For now Get Naked' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)
	if ('Tensai Slime' in item['tags'] or 'Tensei Slime' in item['tags']):
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	return False