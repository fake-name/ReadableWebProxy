

import contextlib
import time

import hiredis
import redis

import config



m_pool = None

def get_redis_conn():
	global m_pool
	if not m_pool:
		m_pool = redis.ConnectionPool(host=config.C_REDIS_SERVER_IP, port=6379, db=0)

	return redis.StrictRedis(connection_pool=m_pool)

def put_redis_conn(conn):
	m_pool.release(conn)



@contextlib.contextmanager
def redis_session_context():

	conn = get_redis_conn()
	try:
		yield conn

	finally:
		pass
		# put_redis_conn(conn)

########################################################################################################################################

q_pool = None

def get_redis_queue_conn():
	global q_pool
	if not q_pool:
		q_pool = redis.ConnectionPool(host=config.C_REDIS_SERVER_IP, port=6379, db=1)

	return redis.StrictRedis(connection_pool=q_pool)

def put_redis_queue_conn(conn):
	q_pool.release(conn)



@contextlib.contextmanager
def redis_queue_session_context():

	conn = get_redis_queue_conn()
	try:
		yield conn

	finally:
		pass
		# put_redis_queue_conn(conn)



########################################################################################################################################

a_pool = None

def get_redis_active_conn():
	global a_pool
	if not a_pool:
		a_pool = redis.ConnectionPool(host=config.C_REDIS_SERVER_IP, port=6379, db=2)

	return redis.StrictRedis(connection_pool=a_pool)

def put_redis_active_conn(conn):
	a_pool.release(conn)



@contextlib.contextmanager
def redis_active_session_context():

	conn = get_redis_active_conn()
	try:
		yield conn

	finally:
		pass
		# put_redis_queue_conn(conn)


FETCHING_URL_SET_NAME = 'fetching-urls'

def put_fetching_url(item):
	with redis_active_session_context() as conn:
		conn.sadd(FETCHING_URL_SET_NAME, item)

def remove_fetching_url(item):
	with redis_active_session_context() as conn:
		conn.srem(FETCHING_URL_SET_NAME, item)

def get_fetching_urls():
	with redis_active_session_context() as conn:
		ret = conn.smembers(FETCHING_URL_SET_NAME)
		ret = list(ret)

	return ret

def clear_fetching_urls():
	with redis_active_session_context() as conn:
		conn.delete(FETCHING_URL_SET_NAME)

PROCESSING_URL_SET_NAME = 'processing-urls'

def put_processing_url(item):
	with redis_active_session_context() as conn:
		conn.sadd(PROCESSING_URL_SET_NAME, item)

def remove_processing_url(item):
	with redis_active_session_context() as conn:
		conn.srem(PROCESSING_URL_SET_NAME, item)

def get_processing_urls():
	with redis_active_session_context() as conn:
		ret = conn.smembers(PROCESSING_URL_SET_NAME)
		ret = list(ret)

	return ret

def clear_processing_urls():
	with redis_active_session_context() as conn:
		conn.delete(PROCESSING_URL_SET_NAME)

########################################################################################################################################

def test():
	put_active_url("test-1")
	put_active_url("test-2")
	put_active_url("test-3")
	put_active_url("test-4")
	put_active_url("test-1")
	remove_active_url("test-3")

	urls = get_active_urls()
	print("Urls:", urls)

	remove_active_url("test-1")
	remove_active_url("test-2")
	remove_active_url("test-3")
	remove_active_url("test-4")
	remove_active_url("test-1")


	urls = get_active_urls()
	print("Urls:", urls)

	# with redis_session_context() as rd:
	# 	print(rd)
	# 	havel = rd.mget(['1', '2', '3'])
	# 	print(havel)

	# 	# Set all the new URLs
	# 	with rd.pipeline(transaction=False) as pipe:
	# 		for url in ['1', '2', '3']:
	# 			pipe.set(url, time.time())
	# 		pipe.execute()

	# 	havel = rd.mget(['1', '2', '3'])
	# 	print(havel)

	# 	print([float(tmp) for tmp in havel])
	with redis_queue_session_context() as rd:
		print(rd)
		print(rd.lpop("test"))
		rd.rpush("test", "lolwat")
		print(rd.lpop("test"))
		rd.rpush("test", None)
		print(rd.lpop("test"))

	with redis_queue_session_context() as rd:
		items = rd.scan_iter("*")
		print(list(items))
		items = rd.scan_iter("raw_*")
		print(list(items))

def config_redis():
	print("Setting redis config")
	with redis_session_context() as redis:
		redis.config_set("auto-aof-rewrite-percentage", 0)
		redis.config_set("save", '')
		redis.config_set("appendonly", "no")
		redis.config_set("maxmemory", "4gb")
		redis.config_set("maxmemory-policy", "allkeys-lru")
	with redis_queue_session_context() as redis:
		redis.config_set("auto-aof-rewrite-percentage", 0)
		redis.config_set("save", '')
		redis.config_set("appendonly", "no")
		redis.config_set("maxmemory", "4gb")
		redis.config_set("maxmemory-policy", "allkeys-lru")
	print("redis configured")


if __name__ == '__main__':
	test()


