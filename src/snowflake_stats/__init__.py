from . import database
from . import stats

SNOWFLAKE_LOG_PATH = "../snow.log"
relayed_data, restart_data = database.get_data(SNOWFLAKE_LOG_PATH)

stats_obj = stats.Stats(relayed_data)
print(str(stats_obj))


def dump_markdown(markdown_path: str):
    stats.dump_markdown(markdown_path, stats_obj)
