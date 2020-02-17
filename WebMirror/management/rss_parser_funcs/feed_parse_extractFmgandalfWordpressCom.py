def extractFmgandalfWordpressCom(item):
	'''
	Parser for 'fmgandalf.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('BS ',       'Black Summoner',                              'translated'),
			('Mitsy',     'Makikomarete Isekai Teni suru Yatsu wa',      'translated'),
			('Gun- Ota ', 'Gun-ota ga Majou Sekai ni Tensei Shitara',    'translated'),
			('Gun OTA ',  'Gun-ota ga Majou Sekai ni Tensei Shitara',    'translated'),
			('Gun-Ota ',  'Gun-ota ga Majou Sekai ni Tensei Shitara',    'translated'),
			('GOGMS ',    'Gun-ota ga Majou Sekai ni Tensei Shitara',    'translated'),
			('SS HH ',    'Self-proclaimed! An Ordinary Demonic Hero’s life ~ The Result of Creating a Cheat Dungeon Despite Being a B-class Demon',    'translated'),
			('SSHH',      'Self-proclaimed! An Ordinary Demonic Hero’s life ~ The Result of Creating a Cheat Dungeon Despite Being a B-class Demon',    'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False