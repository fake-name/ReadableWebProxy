
if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

import json
import Misc.diff_match_patch as dmp
import WebMirror.util.webFunctions as wf

def go():
	wg = wf.WebGetRobust()

	new_content = wg.getpage("https://www.youtube.com/")
	old_content = wg.getpage("https://www.youtube.com/")

	print("Calculating diff")

	differ = dmp.diff_match_patch()

	diff = differ.patch_make(new_content, old_content)
	textdiff = differ.patch_toText(diff)
	# print(textdiff)
	print(len(new_content), len(old_content), len(diff), len(textdiff))
	differ_2 = dmp.diff_match_patch()
	d2     = differ_2.patch_fromText(textdiff)
	old_content_reconstituted, results = differ_2.patch_apply(d2, new_content)

	print(type(old_content_reconstituted))
	print("Succeeded: ", old_content == old_content_reconstituted)


	# err = differ_2.patch_make(new_content, old_content_reconstituted)
	# print(err)
	# print(d2)

	# import code
	# code.interact(local=locals())

	# d = difflib.unified_diff(new_content.splitlines(1), old_content.splitlines(1))
	# diff = "".join(list(d))
	# print(diff)
	# print(len(new_content), type(new_content))
	# print(len(old_content), type(old_content))
	# print(new_content==p2)

	# print(d)
	# print(len(diff))
	# print(wg)


if __name__ == '__main__':
	go()
