# Optimal Location Based Itinerary: CSCI 5654 Final Project

### Install
#### Dependencies:
  * [PuLP](http://pythonhosted.org/PuLP/): ```pip3 install pulp```
  * GLPK: ```sudo apt-get install python-glpk glpk-utils```
  * [Flask](http://flask.pocoo.org/): ```pip3 install flask```
  * Google Maps API: ```pip3 install googlemaps```
  
#### How to Run:
  * ```python3 server.py ```
  * Navigate to [localhost:5000](http://localhost:5000)
  
#### Restrictions:
  * Google Maps API limits the number of API calls; therefore, the max search radius is small.
    * Due to these API call limitations, we make the underlying assumption that the path time from A to B is the same as B to A. This introduces an element of randomness from run to run based on the order Google returns places.
  * We only search through places that are open and will remain open for the time period specified.
  * We only consider travel by car; and therefore, include an automatic time addition of 30 seconds to travel from any point to any other point.
  
  

