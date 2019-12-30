def extractCtrlAlcala(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Chronicles Of Adrian Weiss Chapter'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Starry Heaven Saga: The Chronicles Of Adrian Weiss', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Magical Tournament Volume' in item['title']:
		return buildReleaseMessageWithType(item, 'Magical Tournament: Rise Of The Black Swan', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Type: Hybrid' in item['title']:
		return buildReleaseMessageWithType(item, 'Type: Hybrid', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Elementals:' in item['title'] or 'Elementals Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Elementals: Crystal Garden', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
