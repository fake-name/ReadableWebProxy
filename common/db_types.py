
from sqlalchemy.dialects.postgresql import ENUM


dlstate_enum   = ENUM('new', 'fetching', 'processing', 'complete', 'error', 'removed', 'disabled', 'specialty_deferred', 'specialty_ready', name='dlstate_enum')
itemtype_enum  = ENUM('western', 'eastern', 'unknown',            name='itemtype_enum')
