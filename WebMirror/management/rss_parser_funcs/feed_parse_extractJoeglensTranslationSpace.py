def extractJoeglensTranslationSpace(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Parallel World Pharmacy' in item['tags']:
		chapter = re.search('(?:chapter|chap)\\W*(\\d+)', item['title'], flags=re.IGNORECASE)
		episode = re.search('(?:episode|ep)\\W*(\\d+)', item['title'], flags=re.IGNORECASE)
		if chapter and episode:
			chp = chapter.group(1)
			frag = episode.group(1)
			return buildReleaseMessageWithType(item, 'Parallel World Pharmacy', vol, chp, frag=frag, postfix=postfix)
	if 'Slave Career Planner' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Successful Business of a Slave Career Planner', vol, chp, frag=frag, postfix=postfix)
	if 'Rokudenashi' in item['tags']:
		return buildReleaseMessageWithType(item, 'Akashic Record of a Bastard Magic Instructor', vol, chp, frag=frag, postfix=postfix)
	if 'Otherworld Nation Founding' in item['tags']:
		return buildReleaseMessageWithType(item, 'Otherworld Nation Founding', vol, chp, frag=frag, postfix=postfix)
	if "Nobu's Otherworld Chronicles" in item['tags']:
		return buildReleaseMessageWithType(item, "Mr. Nobu's Otherworld Chronicles", vol, chp, frag=frag, postfix=postfix)
	return False
