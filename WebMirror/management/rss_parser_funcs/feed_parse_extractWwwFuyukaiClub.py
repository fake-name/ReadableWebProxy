def extractWwwFuyukaiClub(item):
	'''
	Parser for 'www.fuyukai.club'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	fuyukai_squatter_re = re.compile(r'www\.fuyukai\.club/[a-z]\d+[A-Z]/')
	if fuyukai_squatter_re.search(item['linkUrl']):
		return None

	
	tagmap = [
		('I\'ve Been Killing Slimes for 300 Years',       'I\'ve Been Killing Slimes for 300 Years',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('I’ve Been Killing Slimes for 300 Years – Chapter ',       'I\'ve Been Killing Slimes for 300 Years',                      'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False