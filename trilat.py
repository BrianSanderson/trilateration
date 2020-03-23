#!/usr/bin/env python
"""
Trilateration of samples recorded as distances to each of three
referenced GPS points. Input file format should be "name", "dist1",
"dist2", "dist3", "long1", "lat1", "long2", "lat2", "long3", "lat3"
where the distances are reported in meters, and the GPS coordinates
are in decimal degrees. See example file 'headless_mv_spatial.csv'

Adapted from a comment on stackoverflow here:
http://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-and-longitude-points-and-3-distances/415#415

The wikipedia entry referenced in the comments is:
http://en.wikipedia.org/wiki/Geodetic_system#geodetic_to.2Ffrom_ECEF_coordinates
"""
import math
import numpy
import argparse
import csv

__author__ = "Brian J. Sanderson <brian@biologicallyrelevant.com"


def trilat(dist_line):
    """
    Takes as an argument a line from the input file (see script docstring for
    expected format) and returns the trilaterated GPS coordinates of the
    sample.
    """
    # assuming elevation = 0
    earthR = 6371
    DistA = float(dist_line[1]) / 1000
    DistB = float(dist_line[2]) / 1000
    DistC = float(dist_line[3]) / 1000
    LatA = float(dist_line[5])
    LonA = float(dist_line[4])
    LatB = float(dist_line[7])
    LonB = float(dist_line[6])
    LatC = float(dist_line[9])
    LonC = float(dist_line[8])

    # using authalic sphere
    # if using an ellipsoid this step is slightly different
    # Convert geodetic Lat/Long to ECEF xyz
    #   1. Convert Lat/Long to radians
    #   2. Convert Lat/Long(radians) to ECEF

    xA = earthR * (math.cos(math.radians(LatA))
                   * math.cos(math.radians(LonA)))
    yA = earthR * (math.cos(math.radians(LatA))
                   * math.sin(math.radians(LonA)))
    zA = earthR * (math.sin(math.radians(LatA)))

    xB = earthR * (math.cos(math.radians(LatB))
                   * math.cos(math.radians(LonB)))
    yB = earthR * (math.cos(math.radians(LatB))
                   * math.sin(math.radians(LonB)))
    zB = earthR * (math.sin(math.radians(LatB)))

    xC = earthR * (math.cos(math.radians(LatC))
                   * math.cos(math.radians(LonC)))
    yC = earthR * (math.cos(math.radians(LatC))
                   * math.sin(math.radians(LonC)))
    zC = earthR * (math.sin(math.radians(LatC)))

    P1 = numpy.array([xA, yA, zA])
    P2 = numpy.array([xB, yB, zB])
    P3 = numpy.array([xC, yC, zC])

    # from wikipedia
    # transform to get circle 1 at origin
    # transform to get circle 2 on x axis

    ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
    i = numpy.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
    ez = numpy.cross(ex, ey)
    d = numpy.linalg.norm(P2 - P1)
    j = numpy.dot(ey, P3 - P1)

    # from wikipedia
    # plug and chug using above values
    x = (math.pow(DistA, 2) - math.pow(DistB, 2) + math.pow(d, 2))/(2*d)
    y = ((math.pow(DistA, 2) - math.pow(DistC, 2)
          + math.pow(i, 2) + math.pow(j, 2))/(2*j)) - ((i/j)*x)

    # only one case shown here
    try:
        z = math.sqrt(math.pow(DistA, 2) - math.pow(x, 2) - math.pow(y, 2))
    except:
        z = float('nan')

    # triPt is an array with ECEF x,y,z of trilateration point
    triPt = P1 + x*ex + y*ey + z*ez

    # convert back to lat/long from ECEF
    # convert to degrees
    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1], triPt[0]))

    # write GPS coordinates for individual out to csv
    return [dist_line[0], lon, lat]


if __name__ == '__main__':
    # Parser for command-line args
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-i', '--input', help='Input file',
                               required=True)
    requiredNamed.add_argument('-o', '--output', help='Output TSV file',
                               required=True)
    args = parser.parse_args()

    # Output csv file
    with open(args.output, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['name', 'long', 'lat'])
        with open(args.input, 'r') as f:
            for line in f:
                out_line = trilat(line.strip().split(','))
                writer.writerow(out_line)
