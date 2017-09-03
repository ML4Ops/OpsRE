CREATE TABLE orbitalObject (
    tPerigee double NOT NULL,
    semiMajorAxis double NOT NULL,
    inclination double NOT NULL,
    eccentricity double NOT NULL,
    rightAscension double NOT NULL,
    argOfPerigee double NOT NULL
);

CREATE TABLE observations (
    tObs double NOT NULL,
    rObs double(3) NOT NULL,
    vObs double(3) NOT NULL,
    hObs double(3) NOT NULL
);
