def extractSereneandTranquil(item):
	"""
	Serene and Tranquil
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

	tagmap = {

		'Hello Heir'                                                                        : 'Hello, Heir',
		'Abandoned Empress'                                                                 : 'Who Dares to Touch My Abandoned Empress',
		'xiao hun palace'                                                                   : 'Xiao Hun Palace',
		'disgraced consort'                                                                 : 'Disgraced Consort',
		'Half-Tried Deity'                                                                  : 'Half-Tried Deity',
		'I Am Not The Wangfei'                                                              : 'I Am Not The Wangfei',
		'Your Majesty Please Calm Down'                                                     : 'Your Majesty Please Calm Down',
		'favored intelligent concubine'                                                     : 'Favored Intelligent Concubine',
		'Beloved Empress'                                                                   : 'Beloved Empress',
		"The Homebody's Lover"                                                              : "The Homebody's Lover",
		'Xian Wang Dotes On Wife'                                                           : 'Xian Wang Dotes On Wife',
		'Refusing to Serve Me? Then Off With Your Head'                                     : 'Refusing To Serve Me? Then Off With Your Head!',
		'Refusing To Serve Me? Then Off With Your Head!'                                    : 'Refusing To Serve Me? Then Off With Your Head!',
		'The Favored Intelligent Concubine'                                                 : 'The Favored Intelligent Concubine',
		'Phoenix Overlooking the World - Who Dares to Touch My Abandoned Empress'           : 'Phoenix Overlooking the World - Who Dares to Touch My Abandoned Empress',
		

	}

	for tag, sname in tagmap.items():
		if tag in item['tags']:
			return buildReleaseMessageWithType(item, sname, vol, chp, frag=frag)
		
		
	return False