
import Projectile as proj
import numpy as np

maxObsCount = 100
maxCatalogLength = 100


# define the right metric for differences in orbits
# try using delta of the H values
# only the magnitude of the difference matters
def compareOrbits (h1, h2):
    hDelta = h2 - h1
    hDeltaMag = np.linalg.norm(hDelta)
    correlationLimit = 100.
    print 'Compare: ',h1,h2,hDelta,hDeltaMag,correlationLimit
    if (hDeltaMag < correlationLimit):
        correlates = True
    else:
        correlates = False
    return correlates

class Observations:

    obsCount = 0
    objCatalogLength = 0
    
    tObs = np.zeros(maxObsCount)
    rObs = np.zeros((maxObsCount, 3))
    vObs = np.zeros((maxObsCount, 3))
    aCatalog = np.zeros(maxCatalogLength)
    eCatalog = np.zeros(maxCatalogLength)
    iCatalog = np.zeros(maxCatalogLength)
    omega_APCatalog = np.zeros(maxCatalogLength)
    omega_LANCatalog = np.zeros(maxCatalogLength)
    TCatalog = np.zeros(maxCatalogLength)
    h_zeros = np.zeros((3,3))
    hCatalog = maxCatalogLength*h_zeros
    
    print "Initialized observations"
    
    def __init__(self):
        self.obsCount = 0
        self.objCatalogLength = 0
        print "Received observation: ",self.obsCount
   
    def model(self, t, r_obs, v_obs, h_obs):
        print "obsCount: ",self.obsCount
        # Collect observations
        self.tObs[self.obsCount] = t
        self.rObs[self.obsCount] = r_obs
        self.vObs[self.obsCount] = v_obs
        
        self.obsCount = self.obsCount + 1

        # Convert ECI vector to orbital elements
        a,e,i,omega_AP,omega_LAN,T,h = proj.cart_2_kep(t,r_obs,v_obs)

        correlates = False
        print "Compare obs to each of the ",self.objCatalogLength," obs in catalog"
        # Compare orbital elements to existing collection
        for j in range (0, self.objCatalogLength):
                
            # Compare in this order:
            # - Semi-major axis
            correlates = compareOrbits(h, self.hCatalog[j])
            if correlates:
                correlatingObs = j
                break

        # If correlates, then add to orbservation list
        if (correlates):
            # Evaluate statistics of collection
            print "Observation correlates with: ",correlatingObs
            
            # Report anomalies


        # If uncorrelated, create new object
        else:
            print "Add observation to catalog:",self.objCatalogLength
            self.aCatalog[self.objCatalogLength] = a
            self.eCatalog[self.objCatalogLength] = e
            self.iCatalog[self.objCatalogLength] = i
            self.omega_APCatalog[self.objCatalogLength] = omega_AP
            self.omega_LANCatalog[self.objCatalogLength] = omega_LAN
            self.TCatalog[self.objCatalogLength] = T
            self.hCatalog[self.objCatalogLength] = h
            self.objCatalogLength = self.objCatalogLength + 1

