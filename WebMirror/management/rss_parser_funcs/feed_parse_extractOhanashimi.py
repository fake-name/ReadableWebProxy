def extractOhanashimi(item):
	"""
	# Ohanashimi

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if ':' in item['title']:
		postfix = item['title'].split(':', 1)[-1]
	if 'Seijo no Kaifuku Mahou' in item['tags']:
		return buildReleaseMessageWithType(item, 'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite', vol, chp, frag=frag, postfix=postfix)
	if 'Tate no Yuusha' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	if 'No Fatigue' in item['tags'] or item['title'].lower().startswith('nf: '):
		return buildReleaseMessageWithType(item, 'NO FATIGUE ~24 Jikan Tatakaeru Otoko no Tenseitan~', vol, chp, frag=frag, postfix=postfix)
	return False
