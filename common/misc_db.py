
import datetime

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import BigInteger

from sqlalchemy.dialects.postgresql import JSONB

import cachetools

import common.db_base
import common.db_types

from common.db_engine import get_db_session
from common.db_engine import session_context


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################

KV_META_CACHE = cachetools.TTLCache(maxsize=5000, ttl=60 * 5)

class KeyValueStore(common.db_base.Base):
	__tablename__ = 'key_value_store'

	id          = Column(BigInteger, primary_key=True)

	key    = Column(Text, nullable=False, index=True, unique=True)
	value  = Column(JSONB)


def get_from_db_key_value_store(key):
	global KV_META_CACHE
	print("Getting %s from kv store" % (key, ))
	if key in KV_META_CACHE:
		return KV_META_CACHE[key]

	with session_context() as sess:
		have = sess.query(KeyValueStore).filter(KeyValueStore.key == key).scalar()
		if have:
			print("KV store had entry")
			ret = have.value
		else:
			print("KV store did not have entry")
			ret = {}

		sess.commit()

	try:
		KV_META_CACHE[key] = ret
	except KeyError:
		KV_META_CACHE = cachetools.TTLCache(maxsize=5000, ttl=60 * 5)
		KV_META_CACHE[key] = ret

	return ret


def set_in_db_key_value_store(key, new_data):
	global KV_META_CACHE
	print("Setting kv key %s to %s" % (key, new_data))
	if key in KV_META_CACHE:
		if KV_META_CACHE[key] == new_data:
			return

	with session_context() as sess:
		have = sess.query(KeyValueStore).filter(KeyValueStore.key == key).scalar()
		if have:
			if have.value != new_data:
				print("Updating item: ", have, have.key)
				print("	old -> ", have.value)
				print("	new -> ", new_data)
				have.value = new_data
			else:
				print("Item has not changed. Nothing to do!")
		else:
			print("New item: ", key, new_data)
			new = KeyValueStore(
				key   = key,
				value = new_data,
				)
			sess.add(new)

		sess.commit()

	try:
		KV_META_CACHE[key] = new_data
	except KeyError:
		KV_META_CACHE = cachetools.TTLCache(maxsize=5000, ttl=60 * 5)
		KV_META_CACHE[key] = new_data



##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################



class VersionCheckTable(common.db_base.Base):
	__tablename__ = 'version_checked_table'

	url     = Column(Text, nullable=False, index=True, unique=True, primary_key=True)
	checked = Column(DateTime, index=True)


def get_from_version_check_table(url):
	with session_context() as sess:
		have = sess.query(VersionCheckTable).filter(VersionCheckTable.url == url).scalar()
		if have:
			ret = have.url
		else:
			ret = datetime.datetime.min
		sess.commit()

	return ret


def set_in_version_check_table(url, update_date):
	assert isinstance(update_date, datetime.datetime)
	assert update_date <= datetime.datetime.now()

	with session_context() as sess:
		have = sess.query(VersionCheckTable).filter(VersionCheckTable.url == url).scalar()
		if have:
			if have.checked < update_date:
				print("Updating item: ", have, have.url)
				print("	old -> ", have.checked)
				print("	new -> ", update_date)
				have.checked = update_date
			elif have.checked > datetime.datetime.now():
				print("Have date is too recent?: ", have, have.url)
				print("	old -> ", have.checked)
				print("	new -> ", update_date)
				have.checked = update_date
			else:
				print("Item has not changed. Nothing to do!")
		else:
			print("New item: ", url, update_date)
			new = VersionCheckTable(
				url     = url,
				checked = update_date,
				)
			sess.add(new)

		sess.commit()

