
import traceback

class DownloadException(Exception):
	pass

class CannotAccessGDocException(DownloadException):
	pass

class GarbageDomainSquatterException(DownloadException):
	pass

class RetryProcessingException(Exception):
	pass


def getErrorDiv():
	content = '''
<div>
	<h2>Error!</h2>
	<pre>
	{tb}
	</pre>
</div>

	'''.format(tb=traceback.format_exc())
	title = "Error fetching content!"
	cachestate = "Wat"
	return title, content, cachestate
