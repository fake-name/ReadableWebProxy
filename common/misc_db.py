
import datetime
import logging
import copy

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

kv_log = logging.getLogger("Main.KV_Store")

class KeyValueStore(common.db_base.Base):
	__tablename__ = 'key_value_store'

	id          = Column(BigInteger, primary_key=True)

	key    = Column(Text, nullable=False, index=True, unique=True)
	value  = Column(JSONB)


def get_from_db_key_value_store(key):
	global KV_META_CACHE
	kv_log.info("Getting '%s' from kv store", key)
	if key in KV_META_CACHE:
		return KV_META_CACHE[key]

	with session_context('kv_store') as sess:
		have = sess.query(KeyValueStore).filter(KeyValueStore.key == key).scalar()
		if have:
			kv_log.info("KV store had entry")
			ret = have.value
		else:
			kv_log.info("KV store did not have entry")
			ret = {}

		sess.commit()

	return ret


def set_in_db_key_value_store(key, new_data):
	global KV_META_CACHE

	new_s = str(new_data)
	if len(new_s) > 40:
		new_s = new_s[:35] + "..."

	kv_log.info("Setting kv key '%s' to '%s'", key, new_s)
	if key in KV_META_CACHE:
		if KV_META_CACHE[key] == new_data:
			return

	with session_context('kv_store') as sess:
		have = sess.query(KeyValueStore).filter(KeyValueStore.key == key).scalar()
		if have:
			if have.value != new_data:
				kv_log.info("Updating item: '%s', '%s'", have, have.key)
				kv_log.info("	old -> %s", have.value)
				kv_log.info("	new -> %s", new_s)
				have.value = new_data
			else:
				kv_log.info("Item has not changed. Nothing to do!")
		else:
			kv_log.info("New item: '%s', %s", key, new_s)
			new = KeyValueStore(
				key   = key,
				value = new_data,
				)
			sess.add(new)

		sess.commit()

	try:
		KV_META_CACHE[key] = copy.copy(new_data)
	except KeyError:
		KV_META_CACHE = cachetools.TTLCache(maxsize=5000, ttl=60 * 5)
		KV_META_CACHE[key] = copy.copy(new_data)



##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


vc_log = logging.getLogger("Main.VersionCheckStore")

class VersionCheckTable(common.db_base.Base):
	__tablename__ = 'version_checked_table'

	url     = Column(Text, nullable=False, index=True, unique=True, primary_key=True)
	checked = Column(DateTime, index=True)


def get_from_version_check_table(sess, url):
	have = sess.query(VersionCheckTable).filter(VersionCheckTable.url == url).scalar()
	if have:
		ret = have.url
	else:
		ret = datetime.datetime.min
	sess.commit()

	return ret

def set_in_version_check_table(sess, url, update_date):
	assert isinstance(update_date, datetime.datetime)
	assert update_date <= datetime.datetime.now()

	have = sess.query(VersionCheckTable).filter(VersionCheckTable.url == url).scalar()
	if have:
		if have.checked < update_date:
			vc_log("Updating item: %s, %s", have, have.url)
			vc_log("	old -> %s", have.checked)
			vc_log("	new -> %s", update_date)
			have.checked = update_date
		elif have.checked > datetime.datetime.now():
			vc_log("Have date is too recent: %s, %s", have, have.url)
			vc_log("	old -> %s", have.checked)
			vc_log("	new -> %s", update_date)
			have.checked = update_date
		else:
			vc_log("Item has not changed. Nothing to do!")
	else:
		vc_log("New item: %s, %s", url, update_date)
		new = VersionCheckTable(
			url     = url,
			checked = update_date,
			)
		sess.add(new)

	sess.commit()

