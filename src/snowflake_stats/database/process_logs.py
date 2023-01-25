from datetime import datetime

from ..objects import (
    Relayed,
    RelayedData,
    Restart,
    RestartData
)

from .binding import write_restarts, write_relayed_data


DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


def process_line(line: str, relayed_data: RelayedData, restart_data: RestartData):
    line = line.strip()
    if line == "":
        return

    raw_date = line[:19]
    timestamp = datetime.strptime(raw_date, DATE_FORMAT)

    message = line[20:]
    if "NAT type" in message:
        return

    if message == "Proxy starting":
        restart_data.append(Restart(timestamp=timestamp))
        return

    # disgusting but ehh what the hell :3
    message = message[31:]
    connections = int(message[:message.find(" ")])
    message = message[message.find("↑ ")+2:]
    upload = int(message[:message.find(" ")])
    message = message[message.find("↓ ") + 2:]
    download = int(message[:message.find(" ")])

    relayed_data.append(Relayed(timestamp=timestamp, connections=connections, upload=upload, download=download))


def read_logs(path: str):
    relayed_data = RelayedData()
    restart_data = RestartData()

    with open(path, "r") as log_file:
        for line in log_file:
            process_line(line, relayed_data, restart_data)

    write_restarts(restart_data)
    write_relayed_data(relayed_data)
