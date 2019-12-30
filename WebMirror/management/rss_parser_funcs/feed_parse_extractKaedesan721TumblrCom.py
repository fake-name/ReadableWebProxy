def extractKaedesan721TumblrCom(item):
	'''
	Parser for 'kaedesan721.tumblr.com'
	'''
	
	bad_tags = [
				'FanArt', 
				"htr asks", 
				'Spanish translations', 
				'htr anime','my thoughts', 
				'Cats', 
				'answered', 
				'ask meme',
				'relay convos',
				'translation related post',
				'nightmare fuel',
				'htr manga',
				'memes',
				'htrweek',
				'Video Games',
				'Animation',
				'replies',
				'jazz',
				'Music',
		]
	
	if any([bad in item['tags'] for bad in bad_tags]):
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	if "my translations" in item['tags']:
		tagmap = [
			('Hakata Tonkotsu Ramens',       'Hakata Tonkotsu Ramens',                      'translated'),
			('hakata tonktosu ramens',       'Hakata Tonkotsu Ramens',                      'translated'),
			('PRC',       'PRC',                      'translated'),
			('Loiterous', 'Loiterous',                'oel'),
		]
	
		for tagname, name, tl_type in tagmap:
			if tagname in item['tags']:
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False