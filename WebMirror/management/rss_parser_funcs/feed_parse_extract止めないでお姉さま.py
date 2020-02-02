def extract止めないでお姉さま(item):
	"""
	Parser for '止めないで、お姉さま…'
	"""

	badwords = [
			'subs',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'WATTT' in item['tags']:
		return buildReleaseMessageWithType(item, 'WATTT', vol, chp, frag=frag, postfix=postfix)
	return False