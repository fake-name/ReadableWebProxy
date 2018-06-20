# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
from __future__ import print_function
import os
import traceback
import atexit
import textwrap
import weakref
import io

try:
	import __builtin__ as builtins
except ImportError:
	import builtins

class FileMonitor(object):
	"""
	Collect stacktraces of where files are opened, and prints them out before the
	program exits.

	- Has partial support for python3

	Example
	-------

	# BEGIN monitor.py
	from filemonitor import FileMonitor
	FileMonitor().patch()
	f = open('/bin/ls')
	# END monitor.py

	$ python monitor.py
	  ----------------------------------------------------------------------------
	  path = /bin/ls
	  >   File "monitor.py", line 3, in <module>
	  >     f = open('/bin/ls')
	  ----------------------------------------------------------------------------

	Acknowledgements
	----------------
	http://stackoverflow.com/questions/2023608/check-what-files-are-open-in-python
	Solution modified from http://stackoverflow.com/a/2023709. Authored by Claudiu
	"""
	def __init__(self, print_only_open=True):
		self.openfiles = []
		self.oldopen = builtins.open

		self.oldfile = getattr(builtins, 'file', io.FileIO)

		self.do_print_only_open = print_only_open
		self.in_use = False

		class File(self.oldfile):

			def __init__(int_self, *args, **kwargs):
				path = args[0]

				self.oldfile.__init__(int_self, *args, **kwargs)
				if self.in_use:
					return
				self.in_use = True
				self.openfiles.append((weakref.ref(int_self), path, int_self._stack_trace()))
				self.in_use = False

				# Drop all files where the file itself has been GC'ed
				self.openfiles = [tmp for tmp in self.openfiles if tmp[0]()]
				if len(self.openfiles) > 100:
					print("WARNING")
					print("WARNING")
					print("WARNING")
					print("%s open files!" % len(self.openfiles))


			def close(int_self):
				self.oldfile.close(int_self)

			def _stack_trace(int_self):
				try:
					raise RuntimeError()
				except RuntimeError as e:
					stack = traceback.extract_stack()[:-2]
					return traceback.format_list(stack)

		self.File = File

	def patch(self):
		builtins.open = self.File

		try:
			builtins.file = self.File
		except AttributeError:
			pass

		atexit.register(self.exit_handler)

	def unpatch(self):
		builtins.open = self.oldopen
		try:
			builtins.file = self.oldfile
		except AttributeError:
			pass

	def exit_handler(self):
		indent = '  > '
		terminal_width = os.get_terminal_size()[0]
		for fileref, path, trace in self.openfiles:
			if fileref() and fileref().closed and self.do_print_only_open:
				continue
			print("-" * terminal_width)
			print("  {} = {}".format('path', path))
			lines = ''.join(trace).splitlines()
			_updated_lines = []
			for l in lines:
				ul = textwrap.fill(l,
								   initial_indent=indent,
								   subsequent_indent=indent,
								   width=terminal_width)
				_updated_lines.append(ul)
			lines = _updated_lines
			print('\n'.join(lines))
			print("-" * terminal_width)
			print()

if __name__ == '__main__':
	FileMonitor().patch()
	with open("Wat.txt", "wb") as fp:
		pass
	open('/bin/ls')

