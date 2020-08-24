def extractRhinabolla(item):
	"""
	# Rhinabolla

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'draft' in item['title'].lower():
		return None
		
	if 'Hachi-nan Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)
		
	if item['title'].startswith("Cafe "):
		return buildReleaseMessageWithType(item, 'salvation began from cafe', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('salvation began from cafe',       'salvation began from cafe',                      'translated'),
		('Hachi-nan Chapter',               'Hachinan tte, Sore wa nai Deshou!',              'translated'),
		('infinity moe',                    'infinity moe',                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('strongest hokage kakashi', 'strongest hokage kakashi',                'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False