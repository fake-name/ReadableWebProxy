def extractTurb0(item):
	"""
	# Turb0 Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	extr = re.search(' ([A-Z])\\d+', item['title'], flags=re.IGNORECASE)
	if extr:
		if vol and not chp:
			chp, vol = vol, chp
		ep_key = extr.group(1)
		if ep_key == 'S':
			postfix = 'Shun chapter'
		elif ep_key == 'J' or ep_key == 'Y':
			postfix = 'Julius chapter'
		elif ep_key == 'K':
			postfix = 'Katia chapter'
		elif ep_key == 'B':
			postfix = 'Balto chapter'
	if re.search('blood \\d+', item['title'], flags=re.IGNORECASE):
		postfix = 'Blood Chapter'
	if 'kumo desu ga, nani ka?' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Kumo Desu ga, Nani ka?', vol, chp, frag=frag, postfix=postfix)
	if 'kumo desu ka, nani ga?' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Kumo Desu ga, Nani ka?', vol, chp, frag=frag, postfix=postfix)
	if 'kumo desu ga, nani ga?' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Kumo Desu ga, Nani ka?', vol, chp, frag=frag, postfix=postfix)
	if 'world record' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'World Record', vol, chp, frag=frag, postfix=postfix)
		
	if 'kuzu inou' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Kuzu Inou【Ondo wo Kaeru Mono】 no Ore ga Musou suru made', vol, chp, frag=frag, postfix=postfix)
		
		
	return False