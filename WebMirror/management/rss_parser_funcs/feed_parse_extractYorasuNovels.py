def extractYorasuNovels(item):
	"""
	Parser for 'Yorasu Novels'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Fallen God Records' in item['tags']:
		return buildReleaseMessageWithType(item, 'Fallen God Records', vol, chp, frag=frag, postfix=postfix)
	if 'Godly Model Creator' in item['tags']:
		return buildReleaseMessageWithType(item, 'Godly Model Creator', vol, chp, frag=frag, postfix=postfix)
	if 'Super Brain Telekinesis' in item['tags']:
		return buildReleaseMessageWithType(item, 'Super Brain Telekinesis', vol, chp, frag=frag, postfix=postfix)
	if 'hacker' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hacker', vol, chp, frag=frag, postfix=postfix)
	return False
