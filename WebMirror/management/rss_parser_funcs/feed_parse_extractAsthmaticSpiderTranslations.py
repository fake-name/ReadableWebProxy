def extractAsthmaticSpiderTranslations(item):
	"""
	Asthmatic Spider Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Ore to Kawazu-san' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore to Kawazu-san', vol, chp, frag=frag, postfix=postfix)
	if 'Grimoire X Reverse' in item['tags']:
		return buildReleaseMessageWithType(item, 'Grimoire X Reverse', vol, chp, frag=frag, postfix=postfix)
	if 'Grimoire X Rebirth' in item['tags']:
		return buildReleaseMessageWithType(item, 'Grimoire X Rebirth', vol, chp, frag=frag, postfix=postfix)
	if 'Sleep Learning' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sleep Learning', vol, chp, frag=frag, postfix=postfix)
	if 'Grimoire X Rebirth' in item['title']:
		return buildReleaseMessageWithType(item, 'Grimoire X Rebirth', vol, chp, frag=frag, postfix=postfix)
	return False