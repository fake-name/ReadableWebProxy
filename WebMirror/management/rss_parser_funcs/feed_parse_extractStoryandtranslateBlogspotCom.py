def extractStoryandtranslateBlogspotCom(item):
	'''
	Parser for 'storyandtranslate.blogspot.com'
	'''

	if 'Summary' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Oresuki',               'Ore ga Suki nano wa Imōto dakedo Imōto ja nai',               'translated'),
		('cut & paste',           'Living in this World with Cut & Paste',                       'translated'),
		('Homecoming Hero',       'Kikanshita Yuusha no Gojitsudan',                             'translated'),
		('Sura-chan',             'Kikai Megami Sura-chan no Shiiku Nikki',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Homecoming Hero',       'Kikanshita Yuusha no Gojitsudan',      'translated'),
		('Living Cut & Paste :',  'Living in this World with Cut & Paste',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False