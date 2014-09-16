__author__ = 'Hans Burbano<hburbano@bbox.co>'

from datetime import datetime, timedelta
import math
import csv

class GPXDProcessor(object):

    """docstring for GPXDProcessor"""
    # Index of
    START_LAT, START_LON, END_LAT, END_LON, START_TIME, END_TIME, DISTANCE, LAPSE, SPEED, ISIDDLE = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, gpxdata, GTM, minspeed):
        super(GPXDProcessor, self).__init__()
        # Time delta
        self.timedelta = timedelta(hours=GTM)

        self.gpx_data = gpxdata
        # Min_speed that should be considered for
        self.min_speed = minspeed
        # Lapses
        self.lapses = []

        for j in range(0, 10):
            self.lapses.append([])

        if self.validate():
            self.calculate()

    def validate(self):
        """
        This method validates if the Loades GPX has points
        """

        if len(self.gpx_data[0]) > 1:
            return True
        else:
            return False

    def function(self):
        "docstring"
        return self.gpx_data

    def calculate(self):
        """
        This method calculates the lapses data from the local GPX Data
        """
        data_count = len(self.gpx_data[0])
        dist_conversion = 1000

        temp_time = datetime.strptime(
            self.gpx_data[2][0], "%Y-%m-%dT%H:%M:%SZ")

        temp_time = temp_time + self.timedelta

        for i in range(0, data_count - 1):

            self.lapses[self.START_LAT].append(float(self.gpx_data[0][i]))
            self.lapses[self.START_LON].append(float(self.gpx_data[1][i]))

            self.lapses[self.END_LAT].append(float(self.gpx_data[0][i + 1]))
            self.lapses[self.END_LON].append(float(self.gpx_data[1][i + 1]))

            self.lapses[self.START_TIME].append(temp_time)

            temp_time = datetime.strptime(
                self.gpx_data[2][i + 1], "%Y-%m-%dT%H:%M:%SZ")

            temp_time = temp_time + self.timedelta

            self.lapses[self.END_TIME].append(temp_time)
            self.lapses[self.LAPSE].append(
                self.lapses[self.END_TIME][i] - self.lapses[self.START_TIME][i])
            self.lapses[self.DISTANCE].append(
                haversine(
                    self.lapses[self.START_LAT][i],
                    self.lapses[self.START_LON][i],
                    self.lapses[self.END_LAT][i],
                    self.lapses[self.END_LON][i]) * dist_conversion)
            temp_speed = self.lapses[self.DISTANCE][
                i] / self.lapses[self.LAPSE][i].total_seconds()
            self.lapses[self.SPEED].append(temp_speed)

            if temp_speed < self.min_speed:
                self.lapses[self.ISIDDLE].append(True)
            else:
                self.lapses[self.ISIDDLE].append(False)

    def to_cvs(self, txt):
        """
        docstring of toCVS
        """
        with open(txt, 'w', newline='') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar=',', quoting=csv.QUOTE_NONE)
            spam_writer.writerow(
                ["START_LAT", "START_LON", "END_LAT", "END_LON", "START_TIME", "END_TIME", "DISTANCE", "LAPSE", "SPEED", "IS_IDDLE"])

            for i in range(0, len(self.lapses[0])):
                spam_writer.writerow([self.lapses[self.START_LAT][i],
                                      self.lapses[self.START_LON][i],
                                      self.lapses[self.END_LAT][i],
                                      self.lapses[self.END_LON][i],
                                      self.lapses[self.START_TIME][i],
                                      self.lapses[self.END_TIME][i],
                                      self.lapses[self.DISTANCE][i],
                                      self.lapses[self.LAPSE][i],
                                      self.lapses[self.SPEED][i],
                                      self.lapses[self.ISIDDLE][i]])


def haversine(lat1, lon1, lat2, lon2):
    """
    This method uses the Haversine formula to calculate the distance
    between two coordinates.
    """
    # Earth radius in Km
    e_radius = 6367
    # convert decimal degrees to radians
    lon1 = math.radians(lon1)
    lat1 = math.radians(lat1)
    lon2 = math.radians(lon2)
    lat2 = math.radians(lat2)

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    # Haversine formula
    d_isa = math.sin(d_lat / 2) ** 2 + math.cos(
        lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    ang_c = 2 * math.asin(math.sqrt(d_isa))

    dist = e_radius * ang_c
    return dist
