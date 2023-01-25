import numpy as np
from datetime import datetime

from ..objects import RelayedData

DAY_NAMES = [
    "Monday ",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


class Stats:
    def __init__(self, relayed_data: RelayedData):
        self.relayed_data = relayed_data

        self.timestamps = np.array([relayed.timestamp for relayed in self.relayed_data.hourly_infos])
        self.connections = np.array([relayed.connections for relayed in self.relayed_data.hourly_infos])
        self.uploads = np.array([relayed.upload for relayed in self.relayed_data.hourly_infos])
        self.downloads = np.array([relayed.download for relayed in self.relayed_data.hourly_infos])

        self.connections_hour: list = list()
        self.uploads_hour: list = list()
        self.downloads_hour: list = list()

        self.connections_week: list = list()
        self.uploads_week: list = list()
        self.downloads_week: list = list()

        self.analyze_time_specific()

    total_connections = property(fget=lambda self: np.sum(self.connections))
    total_uploads = property(fget=lambda self: np.sum(self.uploads))
    total_downloads = property(fget=lambda self: np.sum(self.downloads))

    average_connections = property(fget=lambda self: np.average(self.connections))
    average_uploads = property(fget=lambda self: np.average(self.uploads))
    average_downloads = property(fget=lambda self: np.average(self.downloads))

    def analyze_time_specific(self):
        connections_hour = [np.empty(0, dtype=np.int8) for _ in range(24)]
        uploads_hour = [np.empty(0) for _ in range(24)]
        downloads_hour = [np.empty(0) for _ in range(24)]

        connections_week: list = [np.empty(0, dtype=np.int8) for _ in range(7)]
        uploads_week: list = [np.empty(0) for _ in range(7)]
        downloads_week: list = [np.empty(0) for _ in range(7)]

        for relayed in self.relayed_data:
            timestamp: datetime = relayed.timestamp

            connections_hour[timestamp.hour] = np.append(connections_hour[timestamp.hour], relayed.connections)
            uploads_hour[timestamp.hour] = np.append(uploads_hour[timestamp.hour], relayed.upload)
            downloads_hour[timestamp.hour] = np.append(downloads_hour[timestamp.hour], relayed.download)

            connections_week[timestamp.weekday()] = np.append(connections_week[timestamp.weekday()],
                                                              relayed.connections)
            uploads_week[timestamp.weekday()] = np.append(uploads_week[timestamp.weekday()], relayed.upload)
            downloads_week[timestamp.weekday()] = np.append(downloads_week[timestamp.weekday()], relayed.download)

        self.connections_hour = connections_hour
        self.uploads_hour = uploads_hour
        self.downloads_hour = downloads_hour

        self.connections_week = connections_week
        self.uploads_week = uploads_week
        self.downloads_week = downloads_week

    average_connections_by_hour = property(fget=lambda self: [np.average(i) for i in self.connections_hour])
    average_uploads_by_hour = property(fget=lambda self: [np.average(i) for i in self.uploads_hour])
    average_downloads_by_hour = property(fget=lambda self: [np.average(i) for i in self.downloads_hour])

    average_connections_by_week = property(fget=lambda self: [np.average(i) for i in self.connections_week])
    average_uploads_by_week = property(fget=lambda self: [np.average(i) for i in self.uploads_week])
    average_downloads_by_week = property(fget=lambda self: [np.average(i) for i in self.downloads_week])

    def get_markdown(self):
        precision = 2

        string = ""

        string += f"# Averages by Hour\n\n Hour | Connections | Uploads ↑ | Downloads ↓\n---|---|---|---\n"
        for i, (connections, uploads, downloads) in enumerate(
                zip(self.average_connections_by_hour, self.average_uploads_by_hour, self.average_downloads_by_hour)):
            string += f"{i % 12 + 1:02} {'PM' if bool(int(i / 12)) else 'AM'} | {connections:.{precision}f} | {uploads * 1e-3:.{precision}f} MB | {downloads * 1e-3:.{precision}f} MB\n"

        string += "\n"

        string += f"# Averages by Week\n\n Weekday | Connections | Uploads ↑ | Downloads ↓\n---|---|---|---\n"
        for i, (connections, uploads, downloads) in enumerate(
                zip(self.average_connections_by_week, self.average_uploads_by_week, self.average_downloads_by_week)):
            string += f"{DAY_NAMES[i]} | {connections:.{precision}f} | {uploads * 1e-3:.{precision}f} MB | {downloads * 1e-3:.{precision}f} MB\n"

        string += "\n"

        string += f"# Totals\n\n Connections | Uploads ↑ | Downloads ↓\n---|---|---\n" \
                  f"{self.total_connections * 1e-3:.{precision}f} thousand | {self.total_uploads * 1e-6:.{precision}f} GB | {self.total_downloads * 1e-6:.{precision}f} GB\n\n" \
                  f"# Global Averages\n\n Connections | Uploads ↑ | Downloads ↓\n---|---|---\n" \
                  f"{self.average_connections:.{precision}f} | {self.average_uploads * 1e-3:.{precision}f} MB | {self.average_downloads * 1e-3:.{precision}f} MB\n\n"
        return string

    def __str__(self):
        precision = 2

        string = ""

        string += f"# Averages by Week\n\n"
        for i, (connections, uploads, downloads) in enumerate(
                zip(self.average_connections_by_week, self.average_uploads_by_week, self.average_downloads_by_week)):
            string += f"{DAY_NAMES[i]}: {connections:.{precision}f} connections: ↑ {uploads * 1e-3:.{precision}f} MB, ↓ {downloads * 1e-3:.{precision}f} MB  \n"

        string += "\n"

        string += f"# Averages by Hour\n\n"
        for i, (connections, uploads, downloads) in enumerate(
                zip(self.average_connections_by_hour, self.average_uploads_by_hour, self.average_downloads_by_hour)):
            string += f"{i:02}: {connections:.{precision}f} connections: ↑ {uploads * 1e-3:.{precision}f} MB, ↓ {downloads * 1e-3:.{precision}f} MB  \n"

        string += "\n"

        string += f"# Totals\n\n" \
                  f"{self.total_connections * 1e-3:.{precision}f} thousand connections: ↑ {self.total_uploads * 1e-6:.{precision}f} GB, ↓ {self.total_downloads * 1e-6:.{precision}f} GB\n\n" \
                  f"# Global Averages\n\n" \
                  f"{self.average_connections:.{precision}f} connections: ↑ {self.average_uploads * 1e-3:.{precision}f} MB, ↓ {self.average_downloads * 1e-3:.{precision}f} MB\n\n"
        return string
