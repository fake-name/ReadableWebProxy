def extractIsekaiTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('dragon knight',           'Dragon Knight',                                                      'translated'),
		('Maou-sama, Retry!',       'Maou-sama, Retry!',                                                  'translated'),
		('QualiA',                  'QualiA – Simply wanting to meet you once more',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	if 'Tsuki ga Michibiku Isekai Douchuu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tsuki ga Michibiku Isekai Douchuu', vol, chp, frag=frag, postfix=postfix)
	if 'World Reformation' in item['tags'] or item['title'].startswith("WR "):
		return buildReleaseMessageWithType(item, 'World Reformation activities of the Dark God — Loving humans so much, I reincarnated in one —', vol, chp, frag=frag, postfix=postfix)
	if 'Double Edge Hero' in item['tags']:
		return buildReleaseMessageWithType(item, 'Double Edge Hero', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False