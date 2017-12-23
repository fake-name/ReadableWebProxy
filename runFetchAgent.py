
import sys
import common.stuck
common.stuck.install_pystuck()

def init_yappi():
	import atexit
	import yappi

	print('[YAPPI START]')
	# yappi.set_clock_type('')
	yappi.start()

	@atexit.register
	def finish_yappi():
		print('[YAPPI STOP]')

		yappi.stop()

		print('[YAPPI WRITE]')

		stats = yappi.get_func_stats()

		for stat_type in ['pstat', 'callgrind', 'ystat']:
			print('writing run_stats.{}'.format(stat_type))
			stats.save('run_stats.{}'.format(stat_type), type=stat_type)

		print('\n[YAPPI FUNC_STATS]')

		print('writing run_stats.func_stats')
		with open('run_stats.func_stats', 'w') as fh:
			stats.print_all(out=fh)

		print('\n[YAPPI THREAD_STATS]')

		print('writing run_stats.thread_stats')
		tstats = yappi.get_thread_stats()
		with open('run_stats.thread_stats', 'w') as fh:
			tstats.print_all(out=fh)

		print('[YAPPI OUT]')

if "new" in sys.argv:
	import FetchAgent2.server
	FetchAgent2.server.main()
else:
	import FetchAgent.server
	# init_yappi()
	FetchAgent.server.main()
