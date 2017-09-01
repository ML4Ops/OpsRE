import Projectile as proj
import Observations as obs
import numpy as np

maxObjCount = 4

obs = obs.Observations()

t = proj.secondOfYear(237.19596243)

p = [None]*maxObjCount

# Initialize objects
for objCount in range (0,maxObjCount):
    
    p[objCount] = proj.Projectile(objCount, "Satellite"+str(objCount))
         
    # initialize element set with this TLE
    # 1 05398U 71067E   17237.19596243  .00000191  00000-0  60767-4 0  9996
    # 2 05398  87.6282 147.4622 0065864  59.7371 301.0323 14.33603389412679   
    # Semi-major axis
    a = 7157.e3
    # eccentricity
    e = 0.0065864
    # inclination
    if (objCount == 1):
        i = proj.deg2radian(1.0)
    else:
        i = proj.deg2radian(87.6282)   
    
    # argument of perigee
    omega_AP = proj.deg2radian(59.7371)
    # right ascension of the acsending node
    if (objCount < 2):
        omega_LAN = proj.deg2radian(147.4622)
    else:
        omega_LAN = proj.deg2radian(147.4622-90.0)
        
    # time of periapse passage
    if (objCount == 3):
        # Object 3 follows Object 2 by 10 degrees
        meanAnomaly = proj.deg2radian(301.0323-10)
    else:
        meanAnomaly = proj.deg2radian(301.0323)
        
    revsPerDay = 14.33603389
    orbitalPeriod = 86400./revsPerDay
    T = t - orbitalPeriod*(meanAnomaly/360)

    p[objCount].kep_init (a,e,i,omega_AP,omega_LAN,T)
    print objCount, "initial elements: ",a,e,i,omega_AP,omega_LAN,T


loop = 0
delta_t = orbitalPeriod/8 # 1
running = True

r_offset = [0., 0., 0.]
v_offset = [0., 0., 0.]

while running:
    for objCount in range (0,3):
        r_true, v_true, h_true = p[objCount].propagate(t)
        print "r,v,h: ",t, r_true, v_true, h_true
    ##    h_bar = np.cross(r_true,v_true)
    ##    h = np.linalg.norm(h_bar)
    ##    r = np.linalg.norm(r_true)
    ##    v = np.linalg.norm(v_true)
    ##    print "H:",h_bar, h, r, v
        
        r_obs, v_obs, h_obs = p[objCount].observe(r_true, v_true, r_offset, v_offset)

        # Convert to element set
        a,e,i,omega_AP,omega_LAN,T,h = proj.cart_2_kep(t,r_obs, v_obs)
        print "Check elements: ",t,a,e,i,omega_AP,omega_LAN,T,h
        
        # Evaluation process
        # - when new data is received compute element set
        # - attempt to correlate element set with previously received data
        # - if correlates, then evaluate statistics of data for this object
        # - determine if any other object represents a collision hazard with this object
        obs.model(t, r_obs, v_obs, h_obs)

    
    t = t + delta_t
    loop = loop + 1

    if loop > 4:
        running = False




