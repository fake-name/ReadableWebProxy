def extractWwwWebnovelCom(item):
	'''
	Parser for 'www.webnovel.com'
	'''
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	# So qidian allowed apparently unverified english-language series to be created.
	# Unsurprisingly, a lot of the new stuff is complete garbage
	garbage_series = [
			'/10459149605038505/',
			'/10422423506034705/',
			'/10444772106039905/',
		]

	if any([tmp in item['linkUrl'] for tmp in garbage_series]):
		return None
		
	
	# I think this got in somehow. I don't remember.
	# Whoops?
	if item['guid'] == 'https://www.webnovel.com/rssbook/7834223205001705/22941777291964503IRAS Chapter 809':
		return None
	
	have = get_feed_article_meta(item['guid'])
	haveold = {key : value for key, value in have.items()}
	
	
	have['language'] = "unknown"
	
	if 'content' in item and item['content']:
		
		if item['content'] and 'value' in item['content'][0] and item['content'][0]['value']:
			metadata = json.loads(item['content'][0]['value'])
			
			ad_free = metadata.get("ad_free", False) 
			if ad_free and not have.get("ad_free", False):
				have['ad_free'] = ad_free
			else:
				print("Item still has ad")
				
				
			resolved_url = metadata.get("resolved_url", None) 
			if resolved_url and resolved_url != have.get("resolved_url", None):
				have['resolved_url'] = resolved_url
			else:
				print("Correct URL not resolved properly")
			
			series_name = metadata.get("series_name", None)
			if series_name:
				have['series_name'] = series_name
			series_type = metadata.get("type", None)
			if series_type:
				have['type'] = series_type
	
			
			have['language'] = metadata.get("bookInfo", {}).get("languageName", "unknown")
			

	if not 'ad_free' in have:
		print("Missing ad entry entirely")
		have['ad_free'] = False
		
	if not have['ad_free']:
		print("Not ad-free!")
		set_feed_article_meta(item['guid'], have)
		
		
	
	if not 'resolved_url' in have:
		print("No resolved URL")
		have['resolved_url'] = None
		
	if haveold != have:
		print("Item metadata has changed! Doing commit!")
		set_feed_article_meta(item['guid'], have)
		
	
	if not have['resolved_url']:
		print("Resolved URL isn't valid")
		return False
	
	if "/rssbook/" in have['resolved_url']:
		print("/rssbook/ entry made it through to resolved_url")
		return False
		
	item['linkUrl'] = have['resolved_url']
	
	if have['language'] != 'en':
		print("Non english content (%s). Ignoring" % (have['language'], ))
		return False
	
	if 'type' in have and 'series_name' in have:
	
		print("Resolved metadata:", have)
		if have['type'] in ['translated', 'oel']:
			if have['ad_free']:
				print("Have remote release update metadata!")
				return buildReleaseMessageWithType(item, have['series_name'], vol, chp, frag=frag, postfix=postfix, tl_type=have['type'])
			else:
				return buildReleaseDeleteMessageWithType(item, have['series_name'], vol, chp, frag=frag, postfix=postfix, tl_type=have['type'], prefixMatch=True)
		else:
			print("Type and series_name in have, but type is not a known value?", have)
				
				

	return False