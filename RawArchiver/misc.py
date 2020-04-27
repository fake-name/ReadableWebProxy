

import xxhash
import urllib.parse
import RawArchiver.RawActiveModules
import common.util.rewalk_epoch

class UnwantedUrlError(RuntimeError):
	pass

def getModuleForUrl(url):

	for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
		# print("Module:", module, module.cares_about_url)
		if module.cares_about_url(url):
			return module
	raise UnwantedUrlError("Unwanted URL: %s" % url)


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

def get_interval_for_url(url):

	for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
		# print("Module:", module, module.cares_about_url)
		if module.cares_about_url(url):
			return module.rewalk_interval

	return 0

def get_epoch_for_url(url, netloc):
	interval = get_interval_for_url(url)
	assert netloc

	# If the url isn't wanted, set the epoch to never
	if interval == 0:
		return 2**30
	return common.util.rewalk_epoch.get_epoch_from_netloc_interval(netloc, interval)


