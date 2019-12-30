def extract鏡像翻訳(item):
	"""
	Parser for '鏡像翻訳'
	"""
	
	if 'anime' in str(item['tags']).lower():
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('sodachi fiasco',       'Orokamonogatari - Sodachi Fiasco',                      'translated'),
		('karen ogre',           'Wazamonogatari - Karen Ogre',                           'translated'),
		('shinobu mustard',      'Shinobumonogatari - Shinobu Mustard',                   'translated'),
		('tsubasa sleeping',     'Wazamonogatari - Tsubasa Sleeping',                     'translated'),
		('acerola bon appetit',  'Wazamonogatari - Acerola Bon Appetit',                  'translated'),
		('tsudzura human',       'Musubimonogatari - Tsudzura Human',                     'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('jinrui saikyou no netsuai',        'Jinrui Saikyou no Netsuai',         'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False