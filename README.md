# Optimal Location Based Itinerary

## Authors
### Sean Donohoe
### Kyle Wiese

## Description
This package contains a linear program which solves for an optimal "valued" route through a set of locations taken from the Google Places API. It attempts to maximize the value of a particular trip, where the value for visiting any location is the amount of time spent at this location, multiplied by it's average rating. The user may specify specific categories of places to visit, an amount of time available to visit various locations, and more specific constraints for each category of place, such as visiting exactly two places which fall under a specific category. This relies on subtour elimination to find an optimal tour from the specified starting address, through a set of locations, and returning home, all while maintaining time, budget, and category constraints.

The only code which might reflect implementations found on the internet is the initialization of the linear program in value_solver.py, as the PuLP tutorials were referenced for the initial creation of the solver. All other code is unique to this project.

## Install
#### Dependencies:
  * [PuLP](http://pythonhosted.org/PuLP/): ```pip3 install pulp```
  * GLPK: ```sudo apt-get install python-glpk glpk-utils```
  * [Flask](http://flask.pocoo.org/): ```pip3 install flask```
  * Google Maps API: ```pip3 install googlemaps```
  * Asyncio: ```pip3 install asyncio```
  
#### How to Run:
  * ```python3 server.py ```
  * Navigate to [localhost:5000](http://localhost:5000)
  
#### Restrictions:
  * Google Maps API limits the number of API calls; therefore, the max search radius is small.
    * Due to these API call limitations, we make the underlying assumption that the path time from A to B is the same as B to A. This introduces an element of randomness from run to run based on the order Google returns places.
  * We only search through places that are open and will remain open for the time period specified.
  * We only consider travel by car; and therefore, include an automatic time addition of 30 seconds to travel from any point to any other point.

