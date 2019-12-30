def extractKudarajin(item):
	"""
	Kudarajin
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'I Appear to have been Reincarnated as a Love Interest in an Otome Game' in item['tags'] or item['title'].startswith(
	    'I Appear to have been Reincarnated as a Love Interest in an Otome Game: '):
		return buildReleaseMessageWithType(item, 'I Appear to have been Reincarnated as a Love Interest in an Otome Game', vol, chp, frag=frag, postfix=postfix)
	if 'Hokuou Kizoku to Moukinzuma no Yukiguni Karigurashi' in item['tags'] or item['title'].startswith('Hokuou Kizoku to Moukinzuma no Yukiguni Karigurashi:'):
		return buildReleaseMessageWithType(item, 'Hokuou Kizoku to Moukinzuma no Yukiguni Karigurashi', vol, chp, frag=frag, postfix=postfix)
	if 'Miniature Garden Chemister' in item['tags']:
		return buildReleaseMessageWithType(item, 'Miniature Garden Chemister', vol, chp, frag=frag, postfix=postfix)
	if 'Tensei Shite Inaka de Slowlife wo\xa0Okuritai' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tensei Shite Inaka de Slowlife wo\xa0Okuritai', vol, chp, frag=frag, postfix=postfix)
	return False
