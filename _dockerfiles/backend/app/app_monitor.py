import statsd
from app.db.settings import STATSD_HOST
statsd_client = statsd.StatsClient(STATSD_HOST, 8125, prefix='ncirl.pgdcloud.devsecops')
