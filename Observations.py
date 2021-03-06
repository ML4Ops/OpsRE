
import Projectile as proj
import numpy as np

maxObsCount = 100
maxCatalogLength = 100

def rangeCheck(r1, r2):
    rDelta = r2 - r1
    rDeltaMag = np.linalg.norm(rDelta)
    conjunctionLimit = 1000.
    if (rDeltaMag < conjunctionLimit):
        conjunction = True
    else:
        conjunction = False
    return conjunction, rDelta,rDeltaMag
    
# define the right metric for differences in orbits
# try using delta of the H values
# only the magnitude of the difference matters
def compareOrbits (h1, h2, r1, r2):
    hDelta = h2 - h1
    hDeltaMag = np.linalg.norm(hDelta)
    rDelta = r2 - r1
    rDeltaMag = np.linalg.norm(rDelta)
    
    correlationLimit = 100.
    conjunctionLimit = 1000.

    if (hDeltaMag < correlationLimit) and (rDeltaMag < conjunctionLimit):
        correlates = True
    else:
        correlates = False
    # print 'Compare: ',correlates,h1,h2,hDelta,hDeltaMag,correlationLimit
    return correlates, hDelta, hDeltaMag

class Observations:

    obsCount = 0
    objCatalogLength = 0
    conjunctionCount = 0
    correlatingObsCount = 0
    
    tObs = np.zeros(maxObsCount)
    rObs = np.zeros((maxObsCount, 3))
    vObs = np.zeros((maxObsCount, 3))
    aCatalog = np.zeros(maxCatalogLength)
    eCatalog = np.zeros(maxCatalogLength)
    iCatalog = np.zeros(maxCatalogLength)
    omega_APCatalog = np.zeros(maxCatalogLength)
    omega_LANCatalog = np.zeros(maxCatalogLength)
    TCatalog = np.zeros(maxCatalogLength)
    h_zeros = np.zeros(3)
    rCatalog = np.zeros((maxCatalogLength,3))
    vCatalog = np.zeros((maxCatalogLength,3))
    hCatalog = np.zeros((maxCatalogLength,3))
    
    # print "Initialized observations"
    
    def __init__(self):
        self.obsCount = 0
        self.objCatalogLength = 0
        # print "Received observation: ",self.obsCount
   
    def model(self, t, r_obs, v_obs, h_obs):
        # print "obsCount: ",self.obsCount
        # Collect observations
        self.tObs[self.obsCount] = t
        self.rObs[self.obsCount] = r_obs
        self.vObs[self.obsCount] = v_obs
        
        self.obsCount = self.obsCount + 1

        # Convert ECI vector to orbital elements
        a,e,i,omega_AP,omega_LAN,T,h = proj.cart_2_kep(t,r_obs,v_obs)

        for j in range (0,self.obsCount-1):
            # Evaluate range between object and other objects in the catalog
            conjunction = rangeCheck (r_obs, self.rObs[j])
            if conjunction:
                self.conjunctionCount = self.conjunctionCount + 1
        
        # print "Compare obs to each of the ",self.objCatalogLength," obs in catalog"
        # Compare orbital elements to existing collection
        correlates = False
        
        for j in range (0, self.objCatalogLength):

            # Compare in this order:
            # - Semi-major axis
            correlates,hDelta,hDeltaMag = compareOrbits(h, self.hCatalog[j],\
                                                        r_obs,self.rCatalog[j])
            if correlates:
                correlatingObs = j
                self.correlatingObsCount = self.correlatingObsCount + 1
                break

        # If correlates, then add to observation list
        if (correlates):
            # Evaluate statistics of collection
            # Report anomalies
            print "Observation correlates with: ",correlates,correlatingObs,self.obsCount
        else:
            # If uncorrelated, create new object
            print "Add observation to catalog:",self.objCatalogLength
            self.aCatalog[self.objCatalogLength] = a
            self.eCatalog[self.objCatalogLength] = e
            self.iCatalog[self.objCatalogLength] = i
            self.omega_APCatalog[self.objCatalogLength] = omega_AP
            self.omega_LANCatalog[self.objCatalogLength] = omega_LAN
            self.TCatalog[self.objCatalogLength] = T
            self.hCatalog[self.objCatalogLength] = h
            self.objCatalogLength = self.objCatalogLength + 1

        return self.objCatalogLength, self.conjunctionCount, \
               self.correlatingObsCount 

