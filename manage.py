
import inspect
import sys
import WebMirror.Manage

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

func_prefix = "exposed_"

def load_functions():
	ret = {}
	for name, member in inspect.getmembers(WebMirror.Manage):
		if inspect.isfunction(member) and name.startswith(func_prefix):
			name = name[len(func_prefix):]
			assert name not in ret
			ret[name] = member
	return ret


def print_func(name, func):

	doc = inspect.getdoc(func)

	if not doc:
		print("    {} -> {}".format(name.ljust(25), "UNDOCUMENTED"))
	else:
		doclines = doc.splitlines()
		print("    {}".format(name))
		for line in doclines:
			print("            -> {}".format(line))

	sig = inspect.signature(func)
	if not sig.parameters:
		print("        No arguments")
	else:

		print("        {}".format(sig))
	print()

def print_help():
	print("ReadableWebProxy Management CLI Interface!")
	print("Available functions:")
	farr = load_functions()
	names = list(farr.keys())
	names.sort()

	for name in names:
		print_func(name, farr[name])

def try_call(func, args):
	'''
	Try to call function `func` with passed array of arguments `args`.
	Validates that arguments args are of the correct length.
	'''


	sig = inspect.signature(func)

	if len(sig.parameters) == 0 and len(args) == 0:
		print("No params required: ", func)
		func()
		print("Called!")
		return True

	if len(sig.parameters) == len(args):
		print("Matching param count: ", func)
		func(*args)
		return True

	req_params = [parm for parm in sig.parameters if sig.parameters[parm].default == inspect.Parameter.empty]
	if len(args) >= len(req_params) and len(args) <= len(sig.parameters):
		print("Partial coverage of arguments, including all required: ", args)
		func(*args)
		return True

	return False

def call_func(args):
	print("Looking for function callable with params: '{}'".format(args))
	fname = args[0]
	farr = load_functions()
	if not fname in farr:
		return False

	return try_call(farr[fname], args[1:])


def go():
	if len(sys.argv) > 1:
		have = call_func(sys.argv[1:])
		if not have:
			print_help()
		else:
			return
	else:
		print_help()

if __name__ == "__main__":
	go()
