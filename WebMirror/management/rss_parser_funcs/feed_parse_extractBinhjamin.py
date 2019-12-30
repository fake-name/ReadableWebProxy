def extractBinhjamin(item):
	"""
	# Binhjamin

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (vol or chp or frag or postfix):
		return False
	if ('SRKJ' in item['title'] or 'SRKJ-Sayonara Ryuu' in item['tags']) and (chp or vol):
		return buildReleaseMessageWithType(item, 'Sayonara Ryuusei Konnichiwa Jinsei', vol, chp, frag=frag, postfix=postfix)
	if 'Unborn' in item['title']:
		return buildReleaseMessageWithType(item, 'Unborn', vol, chp, frag=frag, postfix=postfix)
	if 'Bu ni Mi' in item['title'] or '100 Years Of Martial Arts' in item['title']:
		return buildReleaseMessageWithType(item, '100 Years Of Martial Arts', vol, chp, frag=frag, postfix=postfix)
	return False
