# code from https://space.stackexchange.com/questions/19322/converting-orbital-elements-to-cartesian-state-vectors

from astropy.constants import G, M_earth, R_earth
from astropy import units as u
import numpy as np

mu = G.value*M_earth.value
Re = R_earth.value

#Test vectors
r_test = np.array([Re + 600.0*1000, 0, 50])
v_test = np.array([0, 6.5 * 1000, 0])

def deg2radian(d):
    return d*np.pi/180.

def radian2deg(rad):
    return rad*180/np.pi

def secondOfYear(dayOfYear):
    return 86400.0*dayOfYear

def computeOrbitalPeriod(semiMajorAxis):
    period = np.sqrt((semiMajorAxis**3)/mu)
    return period
    

# Keplerian elements
# a - semi-major axis
# e - eccentricity
# i - inclination
# omega_AP - argument of perigee
# omega_LAN - right ascension of the ascending node
# T - time of periapse passage
# EA - eccentric anomaly


# calculations described at http://ccar.colorado.edu/asen5070/handouts/cart2kep2002.pdf

def cart_2_kep(t, r_vec,v_vec):
    #1
    h_bar = np.cross(r_vec,v_vec)
    h = np.linalg.norm(h_bar)
    #2 Compute radius
    r = np.linalg.norm(r_vec)
    # Compute velocity
    v = np.linalg.norm(v_vec)
    #3 Compute the specific energy, E
    E = 0.5*(v**2) - mu/r
    #4 Compute semi-major axis, a
    a = -mu/(2*E)
    #5 Compute eccentricity, e
    e = np.sqrt(1 - (h**2)/(a*mu))
    #6 Compute inclination, i
    i = np.arccos(h_bar[2]/h)
    #7 Compute the right ascension of the ascending node, omega_LAN
    omega_LAN = np.arctan2(h_bar[0],-h_bar[1])
    #8 Compute the argument of latitude
    #beware of division by zero here
    lat = np.arctan2(np.divide(r_vec[2],(np.sin(i))),\
    (r_vec[0]*np.cos(omega_LAN) + r_vec[1]*np.sin(omega_LAN)))
    #9 Compute the true anomaly, nu
    # beware of numerical errors here
    nu = np.arccos(np.round(a*(1 - e**2) - r, decimals = 1)/ \
    np.round(e*r , decimals = 1))
    #10 Compute the argument of periapse, omega_AP
    omega_AP = lat - nu
    #11 Compute the eccentric anomaly, EA
    EA = 2*np.arctan(np.sqrt((1-e)/(1+e)) * np.tan(nu/2))
    #12 Compute the time of periapse passage, T
    period = computeOrbitalPeriod(a)
    T = t - period*(EA - e*np.sin(EA))

    return a,e,i,omega_AP,omega_LAN,T,h_bar

# From http://www.jgiesen.de/kepler/kepler.html
# Iterate on a solution of mean anomaly as a function of 
def eccAnom (ec, m):
    i = 0
    maxIter=30
    delta = 0.00001
    # print ("eccAnom1: ",ec, m)
    # m = 2.0*np.pi*(m-np.floor(m))
    if (ec < 0.):
        E=m
    else:
        E=np.pi
    # print ("eccAnom2: ",E, m)
    F = E - ec*np.sin(m) - m
    
    # print ("eccAnom3: ",F, delta)
    while ((np.abs(F) > delta) and (i<maxIter)):
        E = E - F/(1.0-ec*np.cos(E))
        F = E - ec*np.sin(E) - m
        i = i + 1
        check = E - ec*np.sin(E)
        # print ("eccAnom4: ",E, F, check, m)
    return E

# calculations described at http://ccar.colorado.edu/asen5070/handouts/kep2cart_2002.doc               
def kep_2_cart(t,a,e,i,omega_AP,omega_LAN,T):

    #1 Compute the mean anomaly
    # compute orbital period, n
    n = np.sqrt(mu/(a**3))
    # mean anomaly, M, is the portion of a period since last periapse
    # 
    M = 2*np.pi*n*(t - T)
    #2 - compute eccentric anomaly, EA
    # solve for Kepler's equation with the Newton-Raphson method
    EA = eccAnom(e, M)
    check = EA - e*np.sin(EA)
    # print "ecc, check and mean anomaly: ",EA, check, M,n,(1.0/n),t,T
    #3 
    nu = 2*np.arctan(np.sqrt((1-e)/(1+e)) * np.tan(EA/2))
    #4
    r = a*(1 - e*np.cos(EA))
    #5
    h = np.sqrt(mu*a * (1 - e**2))
    #6
    Om = omega_LAN
    w =  omega_AP
    # print ('nu,r,h,Om,w: ',nu,r,h,Om,w)

    X = r*(np.cos(Om)*np.cos(w+nu) - np.sin(Om)*np.sin(w+nu)*np.cos(i))
    Y = r*(np.sin(Om)*np.cos(w+nu) + np.cos(Om)*np.sin(w+nu)*np.cos(i))
    Z = r*(np.sin(i)*np.sin(w+nu))
    r_vec = [X, Y, Z]
    #print ('x,y,z: ',X,Y,Z)

    #7
    p = a*(1-e**2)

    V_X = (X*h*e/(r*p))*np.sin(nu) - (h/r)*(np.cos(Om)*np.sin(w+nu) + \
    np.sin(Om)*np.cos(w+nu)*np.cos(i))
    V_Y = (Y*h*e/(r*p))*np.sin(nu) - (h/r)*(np.sin(Om)*np.sin(w+nu) - \
    np.cos(Om)*np.cos(w+nu)*np.cos(i))
    V_Z = (Z*h*e/(r*p))*np.sin(nu) + (h/r)*(np.cos(w+nu)*np.sin(i))
    v_vec = [V_X, V_Y, V_Z]

    h_vec = np.cross(r_vec,v_vec)
    
    return r_vec, v_vec, h_vec


class Projectile:
    
    count = 0

    def __init__(self,
                 objNum,
                 objName):

        # Keep count of instances
        # count = count + 1

        # Set time to zero
        t = 0
        
        self.objNum = objNum
        self.objName = objName

    def sv_init(t, r_vec, v_vec):
        self.mode = 'sv'
        self.r_vec = r_vec
        self.v_vec = v_vec
        a,e,i,omega_AP,omega_LAN,T, EA, h_vec = cart_2_kep(t,r_vec,v_vec)
        self.a = a
        self.e = e
        self.i = i
        self.omega_AP = omega_AP
        self.omega_LAN = omega_LAN
        self.T = T
        self.EA = EA
        self.h_vec = h_vec
        return self

    def kep_init (self,a,e,i,omega_AP,omega_LAN,T):
        self.mode = 'kepler'
        self.a = a
        self.e = e
        self.i = i
        self.omega_AP = omega_AP
        self.omega_LAN = omega_LAN
        self.T = T
        return self

    def propagate(self,t):
        # print 'propagate: ',t, self.a,self.e,self.i,self.omega_AP,self.omega_LAN,self.T
        r_vec, v_vec, h_vec = kep_2_cart(t,self.a,self.e,self.i,self.omega_AP,self.omega_LAN,self.T)
        # print 'sv: ',r_vec, v_vec
        return [r_vec, v_vec, h_vec]

    # This observation should optionally include
    # injected signal or noise
    def observe(self, r, v, r_offset, v_offset):
        r_obs = [r[0]+r_offset[0], r[1]+r_offset[1], r[2]+r_offset[2]]
        v_obs = [v[0]+v_offset[0], v[1]+v_offset[1], v[2]+v_offset[2]]
        h_obs = np.cross(r_obs,v_obs)
        return r_obs, v_obs, h_obs

##Two Line Element Set Format
# From: https://www.celestrak.com/columns/v04n03/
# Line 1
# Column	Description
# 01	Line Number of Element Data
# 03-07	Satellite Number
# 08	Classification (U=Unclassified)
# 10-11	International Designator (Last two digits of launch year)
# 12-14	International Designator (Launch number of the year)
# 15-17	International Designator (Piece of the launch)
# 19-20	Epoch Year (Last two digits of year)
# 21-32	Epoch (Day of the year and fractional portion of the day)
# 34-43	First Time Derivative of the Mean Motion
# 45-52	Second Time Derivative of Mean Motion (decimal point assumed)
# 54-61	BSTAR drag term (decimal point assumed)
# 63	Ephemeris type
# 65-68	Element number
# 69	Checksum (Modulo 10)
#   (Letters, blanks, periods, plus signs = 0; minus signs = 1)
# Line 2
# Column	Description
# 01	Line Number of Element Data
# 03-07	Satellite Number
# 09-16	Inclination [Degrees]
# 18-25	Right Ascension of the Ascending Node [Degrees]
# 27-33	Eccentricity (decimal point assumed)
# 35-42	Argument of Perigee [Degrees]
# 44-51	Mean Anomaly [Degrees]
# 53-63	Mean Motion [Revs per day]
# 64-68	Revolution number at epoch [Revs]
# 69	Checksum (Modulo 10)
# 123456789012345678901234567890123456789012345678901234567890123456789
# 1 05398U 71067E   17237.19596243  .00000191  00000-0  60767-4 0  9996
# 2 05398  87.6282 147.4622 0065864  59.7371 301.0323 14.33603389412679


