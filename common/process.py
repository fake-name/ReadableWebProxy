
# import prctl
import threading
import sys
import setproctitle

def name_process(pname):
	if '__pypy__' in sys.builtin_module_names:
		pname = "pypy " + str(pname)
	else:
		pname = "python " + str(pname)

	setproctitle.setproctitle(pname)
	# prctl.set_name(pname)

