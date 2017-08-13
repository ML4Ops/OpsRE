# OpsRE
Prototype Recommendation Engine to Support Operations

Goals:
- Implement an end-to-end prototype demonstrating the concepts in the AMOS Paper "Integrating Machine Learning with Space Operations
- Design the prototype to be extensible

High Level Design:
Model
- Data sets
-- Create simple dataset of objects in orbit around Earth
--- Store those orbits in a SQL database
---- Element sets for orbits
---- Extrapolated positions and simulated (noisy) observations
- Data analysis
-- Implement SparkML regression analysis of the dataset

View
- Publish data view email and FB news feed

Controller
- Accept inputs from users and based on their authorizations implement their requests

