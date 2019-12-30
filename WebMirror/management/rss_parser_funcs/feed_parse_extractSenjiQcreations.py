def extractSenjiQcreations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Sandstorm' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sandstorm Story', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Impact and the Invocation' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Impact and the Invocation', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Other World Driver' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'Other World Driver', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Survivors of the Wild' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'Survivors of the Wild', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Symbiotic Lover' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessageWithType(item, 'Symbiotic Lover', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		
	return False