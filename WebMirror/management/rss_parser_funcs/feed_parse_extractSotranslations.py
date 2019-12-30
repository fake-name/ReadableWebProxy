def extractSotranslations(item):
	"""
	# Supreme Origin Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'hachi-nan chapter' in item['title'].lower() and not 'draft' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)
	if 'the devil of an angel chapter' in item['title'].lower() and not 'draft' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'The Devil of an Angel Chapter', vol, chp, frag=frag, postfix=postfix)
	return False
