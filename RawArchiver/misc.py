
import RawArchiver.RawActiveModules

import xxhash
import urllib.parse

def getModuleForUrl(url):

	for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
		# print("Module:", module, module.cares_about_url)
		if module.cares_about_url(url):
			return module
	raise RuntimeError("Unwanted URL: %s" % url)


def thread_affinity(url, total_worker_count):
	'''
	Ensure only one client ever works on each netloc.
	This maintains better consistency of user-agents
	'''

	# Only limit netlocs if we actually need to.
	if not getModuleForUrl(url).single_thread_fetch(url):
		return True

	netloc = urllib.parse.urlsplit(url).netloc

	m = xxhash.xxh32()
	m.update(netloc.encode("utf-8"))

	nlhash = m.intdigest()
	thread_aff = nlhash % total_worker_count
	# print("Thread affinity:", self.total_worker_count, self.worker_num, thread_aff, self.worker_num == thread_aff)
	return thread_aff
