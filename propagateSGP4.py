from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from math import pow
from math import sqrt
import decimal

class Observer:
    def __init__(self,latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
    def eci (epoch):
        # compute the observer position in ECI space for
        # the specified epoch
        return sv

    def orientation(time, sv):
        # for the given state vector return the range, az and el,
        # with rates for an object with that state vector from
        # the observer location
        observerSV = eci(time)
        # compute the orientation between these two state vectors
        return range, az, el, rdot, adot, edot

##  This script reads a text file of cataloged object's element sets
##  then propagates that element set over a specific time period
##  and computes visilibility to that object from a ground station

# Fix the ground station location
groundStation = Observer(0,0, 180., 0.0)

catalog = []
satcat = []


# Read the file of cataloged objects
tleFileName = '2016-199'
while 1:
    f1 = open('/Users/kevinkelly/Documents/space/data/cat-%s.txt' % tleFileName,'r')
    f1.read('%6d %s %9.6f %9.6f %9.6f %9.6f %9.6f %12.5e %9.6f %9.6f %9.6f\n' %
        (satellite.satnum, satellite.epoch,satellite.inclo,
         satellite.nodeo,satellite.argpo, satellite.mo,satellite.ecco,
         satellite.bstar,
         satellite.no, satellite.ndot,satellite.nddot))
    satcat.append(satellite)
# Read the objects of interest list
interestObjects = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
