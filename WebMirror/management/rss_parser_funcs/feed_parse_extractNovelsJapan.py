def extractNovelsJapan(item):
	"""
	'Novels Japan'
	"""
	if item['title'].endswith(' (Sponsored)'):
		item['title'] = item['title'][:-1 * len(' (Sponsored)')]
	if item['title'].endswith(' and Announcement'):
		item['title'] = item['title'][:-1 * len(' and Announcement')]
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().endswith('loner dungeon'):
		return buildReleaseMessageWithType(item, 'I who is a Loner, Using cheats adapts to the Dungeon', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().endswith('vending machine'):
		return buildReleaseMessageWithType(item, 'I was Reborn as a Vending Machine, Wandering in the Dungeon', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().endswith('login bonus'):
		return buildReleaseMessageWithType(item, 'Skill Up with Login Bonus', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().endswith('lv2 cheat') or item['title'].lower().endswith(
	    'ex-hero candidate’s, who turned out to be a cheat from lv2, laid-back life in another world') or 'Lv2 Cheat' in item['tags']:
		return buildReleaseMessageWithType(item, "Ex-Hero Candidate's, Who Turned Out To Be A Cheat From Lv2, Laid-back Life In Another World", vol, chp, frag=frag, postfix=postfix)
	if 'Second Earth' in item['tags']:
		return buildReleaseMessageWithType(item, 'Second Earth', vol, chp, frag=frag, postfix=postfix)
	if 'Strongest Revolution' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Fierce Revolution ~ The Strongest Organism Which Can Kill the Devil and the Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Loner Dungeon' in item['tags']:
		return buildReleaseMessageWithType(item, 'I who is a Loner, Using cheats adapts to the Dungeon', vol, chp, frag=frag, postfix=postfix)
	if 'Skill Up' in item['tags']:
		return buildReleaseMessageWithType(item, 'Skill Up with Login Bonus', vol, chp, frag=frag, postfix=postfix)
	if 'Isobe Isobee' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isobe Isobee', vol, chp, frag=frag, postfix=postfix)
	if 'Ex-hero' in item['tags']:
		return buildReleaseMessageWithType(item, "Ex-Hero Candidate's, Who Turned Out To Be A Cheat From Lv2, Laid-back Life In Another World", vol, chp, frag=frag, postfix=postfix)
	return False
