from typing import Tuple

from ..objects import RelayedData, RestartData
from . import binding
from . import process_logs

add_logs = process_logs.read_logs


def get_data(log_path: str) -> Tuple[RelayedData, RestartData]:
    process_logs.read_logs(log_path)

    return binding.get_relayed_data(), binding.get_restart_data()
