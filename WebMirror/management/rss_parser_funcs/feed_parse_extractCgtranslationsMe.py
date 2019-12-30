def extractCgtranslationsMe(item):
	'''
	Parser for 'cgtranslations.me'
	'''
	
	if 'Manga' in item['tags']:
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if ('Gifting (Fanfic)' in item['tags'] and 'LN Chapters' in item['tags']) or \
		item['tags'] == ['Gifting (Fanfic)']:
		return buildReleaseMessageWithType(item, 'Gifting this World with Wonderful Blessings!', vol, chp, frag=frag, postfix=postfix)
		
	if 'Gifting (Fanfic)' in item['tags'] and 'explosion' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kono Subarashii Sekai ni Bakuen wo!', vol, chp, frag=frag, postfix=postfix)
	
	if ('KonoSuba' in item['tags'] and 'LN Chapters' in item['tags']):
		return buildReleaseMessageWithType(item, 'KonoSuba', vol, chp, frag=frag, postfix=postfix)
	
	
	return False