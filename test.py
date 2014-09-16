__author__ = 'Hans Burbano<hburbano@bbox.co>'
#!/usr/bin/python
"""
This script gives basic tools to calculate iddle time on a GPX data file.
Iddle time defined as the time in which the speed is below a determinated limit
Tested with GPX from Garmin Astro 320 device.
"""
import xml.sax.saxutils
import xml.sax
import os
import gpxiddletime.gpxloader as gpxloader
import gpxiddletime.gpxdprocessor as gpxdprocessor


def listgpxfiles():
    """
    List files on the current directory
    """
    files = []

    for j in os.listdir('.'):
        if os.path.isfile(j):
            extension = os.path.splitext(j)[1]
            if extension == ".gpx":
                files.append(os.path.abspath(j))
    return files

if __name__ == "__main__":
    IDDLE_SPEED = 1.1
    GMT = -5
    # create an XMLReader
    PARSER = xml.sax.make_parser()
    # turn off namespaces
    PARSER.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler

    for i in listgpxfiles():
        GPX_DATA = i
        HANDLER = gpxloader.GPXLoader()
        PARSER.setContentHandler(HANDLER)
        outfile = GPX_DATA.split(".")[0] + str(".csv")
        #print(datetime.strftime("%A, %d. %B %Y %I:%M%p")) + str(": ") + i + str("-->") + outfile)
        PARSER.parse(GPX_DATA)
        XAS = gpxdprocessor.GPXDProcessor(HANDLER.gpx_data, GMT, IDDLE_SPEED)
        XAS.to_cvs(outfile)
