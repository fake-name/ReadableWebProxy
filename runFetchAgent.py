
import sys
import common.stuck
common.stuck.install_pystuck()

if "grpc" in sys.argv:
	import FetchAgent.server_grpc
	FetchAgent.server_grpc.main()
else:
	import FetchAgent.server
	FetchAgent.server.main()
