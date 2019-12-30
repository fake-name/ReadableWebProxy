def extractCNovelProj(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

		

	tagmap = [
		('Please Be More Serious',       'Please Be More Serious',       'translated'), 
		('Still Not Wanting to Forget',  'Still Not Wanting to Forget',  'translated'), 
		('suddenly this summer',         'Suddenly, This Summer',        'translated'), 
		('mr earnest is my boyfriend',   'Mr. Earnest Is My Boyfriend',  'translated'), 

	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False