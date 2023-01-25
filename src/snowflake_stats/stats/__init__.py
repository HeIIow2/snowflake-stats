import os

from . import stats

MARKDOWN_NAME = "stats.md"

Stats = stats.Stats


def dump_markdown(markdown_path: str, stats_obj: stats.Stats):
    with open(os.path.join(markdown_path, MARKDOWN_NAME), "w") as markdown_file:
        markdown_file.write(stats_obj.get_markdown(markdown_path))
