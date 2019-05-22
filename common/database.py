


from sqlalchemy_continuum_vendored import make_versioned
# make_versioned(user_cls=None)

# Import the DB things.
from common.main_archive_db import WebPages
from common.main_archive_db import WebFiles
from common.main_archive_db import PluginStatus
from common.main_archive_db import NuReleaseItem
from common.main_archive_db import NuResolvedOutbound

from common.raw_archive_db import RawWebPages

from common.rss_func_db import Tags
from common.rss_func_db import Author
from common.rss_func_db import RssFeedPost
from common.rss_func_db import RssFeedUrlMapper
from common.rss_func_db import RssFeedEntry
from common.rss_func_db import QidianFeedPostMeta

from common.misc_db import KeyValueStore
from common.misc_db import get_from_db_key_value_store
from common.misc_db import set_in_db_key_value_store
from common.misc_db import get_from_version_check_table
from common.misc_db import set_in_version_check_table

from common.cookie_db import WebCookieDb

from common.db_engine import get_engine
from common.db_engine import get_db_session
from common.db_engine import delete_db_session
from common.db_engine import session_context

from common.db_constants import DB_REALTIME_PRIORITY
from common.db_constants import DB_HIGH_PRIORITY
from common.db_constants import DB_MED_PRIORITY
from common.db_constants import DB_LOW_PRIORITY
from common.db_constants import DB_IDLE_PRIORITY
from common.db_constants import DB_DEFAULT_DIST
from common.db_constants import MAX_DISTANCE

from common.db_base import Base

from common.redis import redis_session_context

import sqlalchemy as sa
sa.orm.configure_mappers()

# from sqlalchemy_searchable import make_searchable
# make_searchable()
