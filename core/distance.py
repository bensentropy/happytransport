"""
Created on Sat May 24 12:15:24 2014

@author: Yong Ly
"""
import json
import requests
 
# Fixed definitions
GOOGLE_URL = 'http://maps.googleapis.com/maps/api/directions/json?'
TRANSIT_COST_FACTOR = 0.1  # This cost is a statistical estimate per minute based on actual fares
DRIVING_COST_FACTOR = 0.77 # This is an estimate
WALKING_COST_FACTOR = 0
CYCLING_COST_FACTOR = 0
 
# ##################################################################################
# Transit cost functions
# ##################################################################################
 
# total distance travelled
# returns distance in metres
def total_distance(output, travel_mode):
    dist = 0
 
    for route in output['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                if travel_mode == 'ALL':
                    dist = dist+step['distance']['value']
                elif step['travel_mode'] == travel_mode:
                    dist = dist+step['distance']['value']
 
    #print "Total distance travelled by " + travel_mode + ": " + str(dist) + "m"
 
    return dist
 
 
# total time taken
# returns time in seconds
def total_time(output, travel_mode):
    time = 0
 
    for route in output['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                if travel_mode == 'ALL':
                    time = time + step['duration']['value']
                elif step['travel_mode'] == travel_mode:
                    time = time + step['duration']['value']
 
    #print "Total Time travelled by " + travel_mode + ": " + str(time/60) + "minutes"
    return time
 
 
# Determine transit cost
# returns cost in dollars
def get_transit_cost(output):
    time = total_time(output, "TRANSIT")
    transit_cost = time/60 * TRANSIT_COST_FACTOR
    #print "$" + str(transit_cost)
    return transit_cost
 
# generate the routing strings
# returns a string format.
def get_directions(output):
    directions=""
    for route in output['routes']:
      for leg in route['legs']:
        for step in leg['steps']:
          directions = directions + step['html_instructions'] + " " + str((step['duration']['value'])/60) + " minutes\n"
    return directions

# print function for get_output
#   
def print_results(results):
    #print transit
    print "\nRESULTS FOR TAKING PUBLIC TRANSPORT:"
    print "Walking distance: " + str(float((results['transit']['distance_walking']))/1000) + " km"
    print "Walking time: " + str((results['transit']['time_walking'])/60) + " minutes"
    print "Transit distance: " + str(float((results['transit']['distance_transit']))/1000) + " km"
    print "Transit time: " + str((results['transit']['time_transit'])/60) + " minutes"
    print "Total travelling distance: " + str(float((results['transit']['distance']))/1000) + " km"
    print "Total travelling time: " + str((results['transit']['time'])/60) + " minutes"
    print "Total cost: $" + str(results['transit']['cost'])
    #print "Instructions:"
    #print results['transit']['instructions']
    
    #print driving
    print "\nRESULTS FOR DRIVING:"
    print "Total travelling distance: " + str(float((results['driving']['distance']))/1000) + " km"
    print "Total travelling time: " + str((results['driving']['time'])/60) + " minutes"
    print "Total cost: $" + str(results['driving']['cost'])
    #print "Instructions:"
    #print results['driving']['instructions']
        
    #print walking
    print "\nRESULTS FOR WALKING:"
    print "Total travelling distance: " + str(float((results['walking']['distance']))/1000) + " km"
    print "Total travelling time: " + str((results['walking']['time'])/60) + " minutes"
    print "Total cost: $" + str(results['walking']['cost'])
    #print "Instructions:"
    #print results['walking']['instructions']
        
    #print bicyling
    print "\nRESULTS FOR CYCLING:"
    print "Total travelling distance: " + str(float((results['bicycling']['distance']))/1000) + " km"
    print "Total travelling time: " + str((results['bicycling']['time'])/60) + " minutes"
    print "Total cost: $" + str(results['bicycling']['cost'])
    #print "Instructions:"
    #print results['bicycling']['instructions']       
    

# Wrapper function to return different modes of transport
#   
def get_output(origin, destination, arrival_time):
    # Make the Request to Google API
    params = dict(
        origin=origin,
        destination=destination,
        sensor='false',
        mode='',
        arrival_time=arrival_time,
        units='metric',
    )
 
    #create return data
    output = {}
    
    # generate dictionary for driving
    params['mode']='driving'
    data = requests.get(url=GOOGLE_URL, params=params)
    binary = data.content
    google_output = json.loads(binary)
    results={}    
    results['distance'] = total_distance(google_output,"ALL")
    results['time'] = total_time(google_output,"ALL")
    results['cost'] = DRIVING_COST_FACTOR * (float(results['distance'])/1000)   #Calculate  
    results['instructions'] = get_directions(google_output) 
    output['driving'] = results
    
    # generate dictionary for walking
    params['mode']='walking'
    data = requests.get(url=GOOGLE_URL, params=params)
    binary = data.content
    google_output = json.loads(binary)
    results={}    
    results['distance'] = total_distance(google_output,"ALL")
    results['time'] = total_time(google_output,"ALL")
    results['cost'] = WALKING_COST_FACTOR * (float(results['distance'])/1000)   #Calculate    
    results['instructions'] = get_directions(google_output)
    output['walking'] = results
   
    # generate dictionary for public transit
    params['mode']='transit'
    data = requests.get(url=GOOGLE_URL, params=params)
    binary = data.content
    google_output = json.loads(binary)
    results={}   
    results['distance'] = total_distance(google_output,"ALL")
    results['time'] = total_time(google_output,"ALL")
    results['cost'] = get_transit_cost(google_output)      
    # transit dictionary gets more results
    results['distance_walking'] = total_distance(google_output,"WALKING")
    results['time_walking'] = total_time(google_output,"WALKING")
    results['distance_transit'] = total_distance(google_output,"TRANSIT")
    results['time_transit'] = total_time(google_output,"TRANSIT")
    results['instructions'] = get_directions(google_output) 
    output['transit'] = results
    
    # generate dictionary for bicyling
    params['mode']='bicycling'
    data = requests.get(url=GOOGLE_URL, params=params)
    binary = data.content
    google_output = json.loads(binary)
    results={}
    results['distance'] = total_distance(google_output,"ALL")
    results['time'] = total_time(google_output,"ALL")
    results['cost'] = CYCLING_COST_FACTOR * (float(results['distance'])/1000)   #Calculate    
    results['instructions'] = get_directions(google_output) 
    output['bicycling'] = results
    return output
 
if __name__ == "__main__":
    # travel mode. values can be: 'transit', 'driving', 'walking', 'bicycling'
    mode = 'transit'
    departure_time='1401138000'
    origin = '6 Vinograd Drive, Te Atatu North, Auckland'
    destination = 'Auckland,NZ'

    results = get_output(origin, destination, departure_time)

    print_results(results)