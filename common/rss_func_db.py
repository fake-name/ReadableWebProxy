

from sqlalchemy import Table

from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

# from  sqlalchemy.sql.expression import func
# from citext import CIText



import common.db_base
import common.db_types

import code
import ast
import astor


from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix



class RssFeedFuncLut(common.db_base.Base):
	__versioned__ = {}

	__tablename__     = 'rss_parser_feed_name_lut'
	name              = 'rss_parser_feed_name_lut'

	id                = Column(BigInteger, primary_key = True, index = True)
	feed_netloc       = Column(Text, nullable = False, index = True)
	feed_id           = Column(BigInteger, ForeignKey('rss_parser_funcs.id'), nullable = False, index = True)

	__table_args__ = (
		UniqueConstraint('feed_netloc', 'feed_id'),
		)

class RssParserFunctions(common.db_base.Base):
	__versioned__ = {}

	__tablename__     = 'rss_parser_funcs'
	name              = 'rss_parser_funcs'

	id                = Column(BigInteger, primary_key = True, index = True)
	version           = Column(Integer, default='0')

	feed_name         = Column(Text, nullable = False, index = True, unique = True)

	enabled           = Column(Boolean, default=True)

	func              = Column(Text)

	__loaded_func       = None

	def get_func(self):
		if self.__loaded_func:
			return self.__loaded_func

		print("Need to load function!")

		func_container = compile(self.func+"\n\n",
				"<db_for_<{}>>".format(self.feed_name), "exec")

		scope = {
			"buildReleaseMessage"              : buildReleaseMessage,
			"extractChapterVolFragment"        : extractChapterVolFragment,
			"extractVolChapterFragmentPostfix" : extractVolChapterFragmentPostfix,
		}
		popkeys = set(scope.keys())
		popkeys.add("__builtins__")

		exec(func_container, scope)

		func = [val for key, val in scope.items() if not key in popkeys]

		# Check we have just one object in the return, and that it's callable
		assert(len(func) == 1)
		assert(callable(func[0]))

		self.__loaded_func = func[0]

		return self.__loaded_func