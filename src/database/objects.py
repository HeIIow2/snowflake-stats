from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple


@dataclass
class Hourly:
    timestamp: datetime
    connections: int
    upload: int
    download: int

    def get_tuple(self):
        return self.timestamp, self.connections, self.upload, self.download



@dataclass
class Relayed:
    hourly_infos: List[Hourly] = field(default_factory=list)

    def get_database_values(self) -> Tuple[tuple]:
        return tuple(hourly_info.get_tuple() for hourly_info in self.hourly_infos)


@dataclass
class Restart:
    timestamp: datetime

    def get_tuple(self):
        return tuple((self.timestamp, ))

@dataclass
class RestartInfo:
    restart_list: List[Restart] = field(default_factory=list)

    def get_database_values(self) -> Tuple[tuple]:
        return tuple(hourly_info.get_tuple() for hourly_info in self.restart_list)
