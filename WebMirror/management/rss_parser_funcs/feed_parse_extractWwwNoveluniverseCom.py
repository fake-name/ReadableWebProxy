def extractWwwNoveluniverseCom(item):
	'''
	Parser for 'www.noveluniverse.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
	
		("Banished Disciple’s Counterattack - Chapter",      "Banished Disciple’s Counterattack",        "translated"), 
		("Cultivation---Stand above the Heaven - Chapter",   "Cultivation---Stand above the Heaven",     "translated"), 
		("Immortal Asura - Chapter",                         "Immortal Asura",                           "translated"), 
		("Killing Gods - Chapter",                           "Killing Gods",                             "translated"), 
		("Magic Love Ring - Chapter",                        "Magic Love Ring",                          "translated"), 
		("Reincarnation of the Heaven - Chapter",            "Reincarnation of the Heaven",              "translated"), 
		("Supernatural Clairvoyant - Chapter",               "Supernatural Clairvoyant",                 "translated"), 
		("Supernatural Monetary System - Chapter",           "Supernatural Monetary System",             "translated"), 
		("The Secret of the Seal - Chapter",                 "The Secret of the Seal",                   "translated"), 
		("The Skyrider - Chapter",                           "The Skyrider",                             "translated"), 
		("The Supreme Dragon Emperor - Chapter",             "The Supreme Dragon Emperor",               "translated"), 

	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False