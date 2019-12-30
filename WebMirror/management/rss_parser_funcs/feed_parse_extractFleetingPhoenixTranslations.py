def extractFleetingPhoenixTranslations(item):
	"""
	Parser for 'Fleeting Phoenix Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = {

		'Star Martial God Technique'                       : 'Star Martial God Technique',
		'Assassin Farmer'                                  : 'Assassin Farmer',
		'Forbidden Love'                                   : 'Forbidden Love',
		'Ling Qi'                                          : 'Ling Qi',
		'Tehe♪ Wolf'                                       : 'Tehe(*´∀`)♪ I Was Picked Up By a Wolf',

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
			
	return False