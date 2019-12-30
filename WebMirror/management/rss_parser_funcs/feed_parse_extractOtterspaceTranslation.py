def extractOtterspaceTranslation(item):
	"""
	# Otterspace Translation

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Elqueeness' in item['title']:
		return buildReleaseMessageWithType(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
	if '[Dark Mage]' in item['title'] or '[DarkMage]' in item['title']:
		return buildReleaseMessageWithType(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Dragon Maken War' in item['title']:
		return buildReleaseMessageWithType(item, 'Dragon Maken War', vol, chp, frag=frag)
	if 'Legend of Legend' in item['title']:
		return buildReleaseMessageWithType(item, 'Legend of Legend', vol, chp, frag=frag)
	if "Seoul Station's Necromancer" in item['title'] or "Seoul Station's Necromancer" in item['tags']:
		return buildReleaseMessageWithType(item, "Seoul Station's Necromancer", vol, chp, frag=frag)
	if 'Dark Mage' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Limitless Dream' in item['tags']:
		return buildReleaseMessageWithType(item, 'Limitless Dream', vol, chp, frag=frag)
	if 'Link the Orc' in item['tags']:
		return buildReleaseMessageWithType(item, 'Link the Orc', vol, chp, frag=frag)
	if 'KON' in item['tags']:
		return buildReleaseMessageWithType(item, 'King of the Night', vol, chp, frag=frag)
	if 'EoSP' in item['tags']:
		return buildReleaseMessageWithType(item, 'Emperor of Solo Play', vol, chp, frag=frag)
	if 'Elqueeness' in item['title']:
		return buildReleaseMessageWithType(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
	if '[Dark Mage]' in item['title'] or '[DarkMage]' in item['title']:
		return buildReleaseMessageWithType(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Dragon Maken War' in item['title']:
		return buildReleaseMessageWithType(item, 'Dragon Maken War', vol, chp, frag=frag)
	if 'Legend of Legend' in item['title']:
		return buildReleaseMessageWithType(item, 'Legend of Legend', vol, chp, frag=frag)
	if "Seoul Station's Necromancer" in item['title'] or "Seoul Station's Necromancer" in item['tags']:
		return buildReleaseMessageWithType(item, "Seoul Station's Necromancer", vol, chp, frag=frag)
	if 'Dark Mage' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Elqueeness' in item['title']:
		return buildReleaseMessageWithType(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
	if '[Dark Mage]' in item['title'] or '[DarkMage]' in item['title']:
		return buildReleaseMessageWithType(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Dragon Maken War' in item['title']:
		return buildReleaseMessageWithType(item, 'Dragon Maken War', vol, chp, frag=frag)
	if 'Legend of Legend' in item['title']:
		return buildReleaseMessageWithType(item, 'Legend of Legend', vol, chp, frag=frag)
	if "Seoul Station's Necromancer" in item['title'] or "Seoul Station's Necromancer" in item['tags']:
		return buildReleaseMessageWithType(item, "Seoul Station's Necromancer", vol, chp, frag=frag)
	if 'Dark Mage' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dark Mage', vol, chp, frag=frag)
	return False