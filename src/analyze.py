import snowflake_stats


snowflake_stats.dump_markdown("../analyzed")
print(str(snowflake_stats.stats_obj))
