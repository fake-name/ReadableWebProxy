
# from app.models import Releases
# from sqlalchemy.sql.expression import nullslast
# from sqlalchemy import desc

from flask.ext.sqlalchemy import Pagination
from flask import abort

# def get_latest_release(series):
# 	latest = Releases                                        \
# 				.query                                       \
# 				.filter(Releases.series==series.id)          \
# 				.filter(Releases.include==True)              \
# 				.order_by(nullslast(desc(Releases.volume)))  \
# 				.order_by(nullslast(desc(Releases.chapter))) \
# 				.limit(1)                                    \
# 				.scalar()

# 	return latest



def paginate(query, page, per_page=20, error_out=True):
	if error_out and page < 1:
		abort(404)
	items = query.limit(per_page).offset((page - 1) * per_page).all()
	if not items and page != 1 and error_out:
		abort(404)

	# No need to count if we're on the first page and there are fewer
	# items than we expected.
	if page == 1 and len(items) < per_page:
		total = len(items)
	else:
		total = query.order_by(None).count()

	return Pagination(query, page, per_page, total, items)


