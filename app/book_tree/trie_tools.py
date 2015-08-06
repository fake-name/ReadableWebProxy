import urllib.parse
import time
import uuid
import settings
import string

from natsort import natsorted

def compact_trie(inKey, inDict):

	if len(inDict) == 0:
		raise ValueError("Wat? Item in dict with zero length!")
	elif len(inDict) == 1:

		curKey, curDict = inDict.popitem()

		# Don't munge the end key
		if curKey == "_end_":
			return inKey, {curKey : curDict}

		curKey, curDict = compact_trie(curKey, curDict)
		return inKey+curKey, curDict

	else:   # len(inDict) > 1

		ret = {}
		for key, value in inDict.items():
			if key != "_end_":
				key, value = compact_trie(key, value)
			ret[key] = value

		return inKey, ret


def build_trie(iterItem, getKey=lambda x: x):
	base = {}


	# Build a trie data structure that represents the strings passed using nested dicts
	scan = []
	for item in iterItem:
		scan.append((getKey(item).lower(), item))

	for key, item in scan:

		floating_dict = base
		for letter in key:
			floating_dict = floating_dict.setdefault(letter, {})
		floating_dict["_end_"] = item

	# Flatten cases where nested dicts have only one item. convert {"a": {"b" : sommat}} to {"ab" : sommat}
	key, val = compact_trie('', base)
	out = {key : val}

	return out

