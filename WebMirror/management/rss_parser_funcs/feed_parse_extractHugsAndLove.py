def extractHugsAndLove(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if not postfix and ':' in item['title']:
		postfix = item['title'].split(':', 1)[-1]
	if 'Felicia Second Life' in item['tags']:
		return buildReleaseMessageWithType(item, 'Felicia Second Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'the rock' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Rock', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('Armageddon'):
		return buildReleaseMessageWithType(item, 'Armageddon', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
