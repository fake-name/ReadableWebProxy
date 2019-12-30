def extractFallentranslationsBlogspotCom(item):
	'''
	Parser for 'fallentranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('I Heard You Like Me Too (',                    'I Heard You Like Me Too',                        'translated'),
		('Being An Author Is A High Risk Occupation (',  'Being An Author Is A High Risk Occupation',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False