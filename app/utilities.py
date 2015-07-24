
from app.models import Releases
from sqlalchemy.sql.expression import nullslast
from sqlalchemy import desc

def get_latest_release(series):
	latest = Releases                                        \
				.query                                       \
				.filter(Releases.series==series.id)          \
				.filter(Releases.include==True)              \
				.order_by(nullslast(desc(Releases.volume)))  \
				.order_by(nullslast(desc(Releases.chapter))) \
				.limit(1)                                    \
				.scalar()

	return latest

