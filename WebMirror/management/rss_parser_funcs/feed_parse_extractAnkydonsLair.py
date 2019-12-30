def extractAnkydonsLair(item):
	"""
	"Ankydon's Lair"
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Outcast Magician And The Power Of Heretics' in item['tags']:
		return buildReleaseMessageWithType(item, 'Outcast Magician And The Power Of Heretics', vol, chp, frag=frag, postfix=postfix)
	if 'Reincarnation into the Barrier Master' in item['tags']:
		return buildReleaseMessageWithType(item, 'Reincarnation into the Barrier Master', vol, chp, frag=frag, postfix=postfix)
	return False
