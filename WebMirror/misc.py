

import xxhash
import urllib.parse
from WebMirror.rules import load_rules
import common.util.rewalk_epoch

class UnwantedUrlError(RuntimeError):
	pass


def load_nl_refetch_interval_mapping():
	rules = load_rules()


	ret = {}

	for ruleset in rules:
		interval = ruleset['rewalk_interval_days']
		if ruleset['rewalk_disabled']:
			interval = 0

		if ruleset['netlocs']:
			for nl in ruleset['netlocs']:
				ret[nl] = interval

	return ret

nl_refetch = load_nl_refetch_interval_mapping()

def get_interval_for_netloc(netloc):
	if netloc in nl_refetch:
		return nl_refetch[netloc]

	return 0

def get_epoch_for_url(url, netloc=None):
	if not netloc:
		netloc = urllib.parse.urlsplit(url).netloc

	interval = get_interval_for_netloc(netloc)
	assert netloc

	# If the url isn't wanted, set the epoch to never
	if interval == 0:
		return 2**30
	return common.util.rewalk_epoch.get_epoch_from_netloc_interval(netloc, interval)


