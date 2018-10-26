

import contextlib
import time

import hiredis
import redis

import settings



m_pool = redis.ConnectionPool(host=settings.REDIS_SERVER_IP, port=6379, db=0)

def get_redis_conn():
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



q_pool = redis.ConnectionPool(host=settings.REDIS_SERVER_IP, port=6379, db=1)

def get_redis_queue_conn():
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

def test():
	with redis_session_context() as rd:
		print(rd)
		havel = rd.mget(['1', '2', '3'])
		print(havel)

		# Set all the new URLs
		with rd.pipeline(transaction=False) as pipe:
			for url in ['1', '2', '3']:
				pipe.set(url, time.time())
			pipe.execute()

		havel = rd.mget(['1', '2', '3'])
		print(havel)

		print([float(tmp) for tmp in havel])
	with redis_queue_session_context() as rd:
		print(rd)
		print(rd.lpop("test"))
		rd.rpush("test", "lolwat")
		print(rd.lpop("test"))
		rd.rpush("test", None)
		print(rd.lpop("test"))

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
	pass

config_redis()

if __name__ == '__main__':
	test()
