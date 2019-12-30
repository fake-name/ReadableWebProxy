def extractPracticalguidetoevilWordpressCom(item):
	'''
	Parser for 'practicalguidetoevil.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	# Don't have volume information, cannot extract.
	
	return None