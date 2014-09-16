__author__ = 'Hans Burbano<hburbano@bbox.co>'

import xml.sax.saxutils
import xml.sax


class GPXLoader(xml.sax.handler.ContentHandler):

    """
    This class loads in to memory the GPX [lat, lon, time] data generated
    from a Garmin GPS device, uses
    """

    def __init__(self):
        super(GPXLoader, self).__init__()
        # XML List of current tags
        self.tag_list = []
        # Data
        self.gpx_data = []
        # Latitude Data
        self.gpx_data.append([])
        # Longitude Data
        self.gpx_data.append([])
        # Time
        self.gpx_data.append([])
        # Char Buffer
        self.char_buffer = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.tag_list.append(tag)
        self.char_buffer = ""
        if tag == "trkpt":
            self.gpx_data[0].append(attributes["lat"])
            self.gpx_data[1].append(attributes["lon"])

    # Call when element ends
    def endElement(self, name):

        if self.tag_list[-1] == "time":
            if self.tag_list[-2] == "trkpt":
                if self.tag_list[-3] == "trkseg":
                    self.gpx_data[2].append(self.char_buffer)
        del self.tag_list[-1]

    # This method writes the character content to the buffer
    def characters(self, content):
        self.char_buffer += str(content)
