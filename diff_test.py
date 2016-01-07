
if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

import difflib
import WebMirror.util.webFunctions as wf

def go():
	wg = wf.WebGetRobust()

	p1 = wg.getpage("https://www.google.com/")
	p2 = wg.getpage("https://www.google.com/")

	print("Calculating diff")
	d = difflib.unified_diff(p1.splitlines(1), p2.splitlines(1))
	diff = "".join(list(d))
	print(diff)
	print(len(p1), type(p1))
	print(len(p2), type(p2))
	print(p1==p2)

	print(d)
	print(len(diff))
	print(wg)


if __name__ == '__main__':
	go()
