def extractAcidtranslationCom(item):
	'''
	Parser for 'acidtranslation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if (item['tags'] == ['translation'] or item['tags'] == ['Uncategorized']) and item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, 'Rebirth: Degenerate Slave Abuses Tyrant', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
		
	
	
	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False