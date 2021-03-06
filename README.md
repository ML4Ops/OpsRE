# OpsRE
Prototype Recommendation Engine to Support Operations

Goals:
- Implement an end-to-end prototype demonstrating the concepts in the AMOS Paper "Integrating Machine Learning with Space Operations"
- Design the prototype system that emulates an actual operational problem based on a realistic (if simplied) model to demonstrate the integration of machine learning into an operational problem.  It is designed to be extensible so higher fidelity models can be used, or models for other environments, without major changes to the software.
- The user interface should take advantage of the processed data, such as the pattern recognition and anomaly detection capabilities of the machine learning algorithms.
- The processing should architected such that it is relatively straightforward to take advantage of parallellized algorithms

High Level Design:
Model
- Data sets
-- Create simple dataset of objects in orbit around Earth
--- Store those orbits in a SQL database
---- Element sets for orbits
---- Extrapolated positions and simulated (noisy) observations
- Data analysis
-- Implement SparkML regression analysis of the dataset
  - compute minimum distance between objects in orbit
  - create lists of objects that approach meet some criteria based on their min distance, sort by min distance and by number of occurances of that object in the list

View
- Publish data view email and FB news feed
- Define graph that present the picture of the satellites and orbits (via GoogleEarth?) 

Controller
- Accept inputs from users and based on their authorizations implement their requests

Outer Layer
- Standardize structure around the application for integrated testing, training and exercises
- Consists of three major components
-- White Team: manage application configuration and execution, performance evaluation
-- Red Team: provide data feeds, both live, archive and simulation
-- Blue Team: operators.  May be live personnel or emulated.  Roles and responsibilities in three main catagories
--- Strategic: define goals
--- Operations: convert strategic goals to tactical taskings, allocate resources
--- Tactical: execute tasking, monitor data
- All components are modeled by the Actor object class.  Actor objects are defined with specific roles and credentials and can execute stored procedures, based on specific conditions, including user inputs or alerts generated by the data processing subsystem

Define the whole game
- The system is designed to remove orbital debris by momentum transfer to small satellites so that they can be lofted to higher orbits.
- The concept is for small satellites to be launched such that they come close to large debris objects, like rocket bodies, attach a long cable to the rocket body and then rotate around a center of mass.  The object releases the cable at a point in the rotation that optimizes the loft of the satellite and the decay of the rocket body.
- For efficiency, the satellites are launched by an electric rail gun near the equator (for example, the Marshall Islands, the Sahara Desert or the side of Halelakala where the projectile would exit the launch tube at 3 km alt).  
- The simulation consists of rocket bodies in orbit and the player needs to determine which rocket bodies to de-orbit for maximum benefit. 
- Estimate the size of the solar panels needed to charge the electric rail gun to launch the projectile based on one launch per week (or some other period)
- Projectile gets launched into orbit and meets up with the rocket body after N orbits or is launched suborbitally and meets up with the rocket body at apogee. 

References
- Magnetic Launch

http://large.stanford.edu/courses/2012/ph240/thavapatikom2/
https://www.researchgate.net/publication/251861268_StarTram_The_Magnetic_Launch_Path_to_Very_Low_Cost_Very_High_Volume_Launch_to_Space




