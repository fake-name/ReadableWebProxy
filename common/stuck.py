
import runStatus
import threading
import traceback
import sys

def install_pystuck():
	import pystuck
	stuck_port = 6666
	while 1:
		try:
			pystuck.run_server(port=stuck_port)
			print("PyStuck installed to process, running on port %s" % stuck_port)
			return
		except OSError:
			stuck_port += 1
		if stuck_port > 7000:
			raise RuntimeError("wat?")

def halt_exc(x, y):
	if runStatus.run_state.value == 0:
		print("Raising Keyboard Interrupt")
		raise KeyboardInterrupt

def handler(signum, frame):
	for th in threading.enumerate():
		print("Dumping stack for thread: ", th)
		traceback.print_stack(sys._current_frames()[th.ident])
		print()