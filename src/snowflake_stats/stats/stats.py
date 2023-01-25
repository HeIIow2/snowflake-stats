import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

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

def to_am_pm(i) -> str:
    return f"{i % 12 + 1:02} {'PM' if bool(int(i / 12)) else 'AM'}"


class Stats:
    def __init__(self, relayed_data: RelayedData):
        self.relayed_data = relayed_data

        self.timestamps = np.array([relayed.timestamp for relayed in self.relayed_data])
        self.connections = np.array([relayed.connections for relayed in self.relayed_data])
        self.uploads = np.array([relayed.upload for relayed in self.relayed_data])
        self.downloads = np.array([relayed.download for relayed in self.relayed_data])

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

    def draw_diagrams(
            self,
            weekly,
            hourly,
            global_
    ):

        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.errorbar(
            [to_am_pm(i) for i in range(24)],
            self.average_connections_by_hour,
            [np.std(i) for i in self.connections_hour]
        )
        ax1.set_title("Average connections for each Hour")
        ax1.set_ylabel("average connections")
        ax1.tick_params(labelrotation=45)

        ax2.errorbar(
            [to_am_pm(i) for i in range(24)],
            self.average_uploads_by_hour,
            [np.std(i) for i in self.uploads_hour],
            label="uploads in KB"
        )
        ax2.errorbar(
            [to_am_pm(i) for i in range(24)],
            self.average_downloads_by_hour,
            [np.std(i) for i in self.downloads_hour],
            label="downloads in KB"
        )
        ax2.set_title("Average Upload/Download for each Hour")
        ax2.tick_params(labelrotation=45)
        ax2.legend(loc='upper left')
        fig.tight_layout()
        fig.savefig(hourly)

        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.errorbar([DAY_NAMES[i] for i in range(7)], self.average_connections_by_week, [np.std(i) for i in self.connections_week])
        ax1.set_title("Average connections for each Weekday")
        ax1.set_ylabel("average connections")
        ax1.set_xlabel("Weekday")

        ax2.errorbar(
            [DAY_NAMES[i] for i in range(7)],
            self.average_uploads_by_week,
            [np.std(i) for i in self.uploads_week],
            label="uploads in KB"
        )
        ax2.errorbar(
            [DAY_NAMES[i] for i in range(7)],
            self.average_downloads_by_week,
            [np.std(i) for i in self.downloads_week],
            label="downloads in KB"
        )
        ax2.set_title("Average Upload/Download for each Week")
        ax2.tick_params(labelrotation=45)
        ax2.legend(loc='upper left')
        fig.tight_layout()
        fig.savefig(weekly)

        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(self.timestamps, self.connections)
        ax1.set_title("The connections plotted over time")
        ax1.set_ylabel("connections")
        ax1.set_xticks([])

        ax2.plot(self.timestamps, self.uploads, label="downloads in KB")
        ax2.plot(self.timestamps, self.downloads, label="uploads in KB")
        ax2.set_title("Upload/Download over time")
        ax2.set_xticks([])
        ax2.legend(loc='upper left')
        fig.tight_layout()
        fig.savefig(global_)


    def get_markdown(self, markdown_path: str):
        precision = 2
        opening_b = "{"
        closing_b = "}"

        weekly: str = os.path.join(markdown_path, "assets", "weekly_connections.svg")
        hourly: str = os.path.join(markdown_path, "assets", "hourly_connections.svg")
        global_ = os.path.join(markdown_path, "assets", "global_connections.svg")

        self.draw_diagrams(weekly, hourly, global_)

        string = ""

        string += f"# Averages by Hour\n\n![hourly]({hourly}) \n\n Hour | Connections | Uploads ↑ | Downloads ↓\n---|---|---|---\n"
        for i, (connections, uploads, downloads) in enumerate(
                zip(self.average_connections_by_hour, self.average_uploads_by_hour, self.average_downloads_by_hour)):
            string += f"{to_am_pm(i)} | {connections:.{precision}f} | {uploads * 1e-3:.{precision}f} MB | {downloads * 1e-3:.{precision}f} MB\n"

        string += "\n"

        string += f"# Averages by Week\n\n![weekly]({weekly}) \n\n  Weekday | Connections | Uploads ↑ | Downloads ↓\n---|---|---|---\n"
        for i, (connections, uploads, downloads) in enumerate(
                zip(self.average_connections_by_week, self.average_uploads_by_week, self.average_downloads_by_week)):
            string += f"{DAY_NAMES[i]} | {connections:.{precision}f} | {uploads * 1e-3:.{precision}f} MB | {downloads * 1e-3:.{precision}f} MB\n"

        string += "\n"

        string += f"# Totals\n\n ![global]({global_}) \n\n Connections | Uploads ↑ | Downloads ↓\n---|---|---\n" \
                  f"{self.total_connections * 1e-3:.{precision}f} thousand | {self.total_uploads * 1e-6:.{precision}f} GB | {self.total_downloads * 1e-6:.{precision}f} GB\n\n" \
                  f"# Global Averages\n\n  Connections | Uploads ↑ | Downloads ↓\n---|---|---\n" \
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
