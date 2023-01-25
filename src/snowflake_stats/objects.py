from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple


@dataclass
class Relayed:
    """
    This describes the data relayed in one hour
    """
    timestamp: datetime
    connections: int
    upload: int
    download: int

    def get_tuple(self):
        return self.timestamp, self.connections, self.upload, self.download


@dataclass
class RelayedData:
    hourly_infos: List[Relayed] = field(default_factory=list)

    def append(self, hourly: Relayed):
        self.hourly_infos.append(hourly)

    def __iter__(self):
        for relayed in self.hourly_infos:
            yield relayed

    def get_database_values(self) -> Tuple[tuple]:
        return tuple(hourly_info.get_tuple() for hourly_info in self.hourly_infos)


@dataclass
class Restart:
    timestamp: datetime

    def get_tuple(self):
        return tuple((self.timestamp,))


@dataclass
class RestartData:
    restart_list: List[Restart] = field(default_factory=list)

    def append(self, restart: Restart):
        self.restart_list.append(restart)


    def __iter__(self):
        for restart in self.restart_list:
            yield restart

    def get_database_values(self) -> Tuple[tuple]:
        return tuple(hourly_info.get_tuple() for hourly_info in self.restart_list)
