from . import database

SNOWFLAKE_LOG_PATH = "../snow.log"

relayed_data, restart_data = database.get_data(SNOWFLAKE_LOG_PATH)

print(relayed_data)
print(restart_data)
