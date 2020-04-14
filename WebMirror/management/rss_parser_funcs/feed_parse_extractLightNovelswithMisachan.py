def extractLightNovelswithMisachan(item):
	"""
	'Light Novels with Misa-chan~'
	"""
	if item['title'].startswith("Protected:"):
		return None
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	if item['title'].startswith('Ojamajo Doremi Book'):
		return buildReleaseMessageWithType(item, 'Ojamajo Doremi 16', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Ore ga heroine Book'):
		return buildReleaseMessageWithType(item, 'Ore ga heroine wo tasuke sugite sekai ga little apocalypse!?', vol, chp, frag=frag, postfix=postfix)
		
	tagmap = [
		('99th vampire princess',       '99th vampire princess ~The last vampire~',                      'translated'),
		('land mines',                  'Transition to Another World, Land Mines Included',              'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False