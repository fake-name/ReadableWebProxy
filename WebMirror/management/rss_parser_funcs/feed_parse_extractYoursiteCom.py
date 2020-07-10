def extractYoursiteCom(item):
	'''
	Parser for 'yoursite.com'
	
	Note: Feed returns incorrect URLs! Actual site is pbsnovel.rocks
	'''
	
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
		
		
	item['guid'] = item['guid'].replace('http://yoursite.com/', 'http://pbsnovel.rocks/')
	item['linkUrl'] = item['linkUrl'].replace('http://yoursite.com/', 'http://pbsnovel.rocks/')
	
	if not item['title'].startswith("Chapter"):
		return False
	if len(item['tags']) != 1:
		return False
		
	chp_tag = item['tags'][0]
	
	# The items right now have titles that start with "Chapter", and a single tag with the format "int-int"
	# Validate that structure before assuming it's a tag for PBS
	try:
		chp_1, chp_2 = chp_tag.split("-")
		int(chp_1)
		int(chp_2)
		return buildReleaseMessageWithType(item, "Peerless Battle Spirit", vol, chp, frag=frag, postfix=postfix, tl_type='translated')
	except:
		return False
		

	return False