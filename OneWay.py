__author__ = "matthewc"

''' Randy Olson's Shortest Route Program modified By Andrew Liesinger modified by Matthew Carruth'''

from itertools import combinations
import googlemaps
import json
import numpy as np
import os.path
import pandas as pd
import random
import webbrowser
import pdb

CONFIG_FILE = "roadtripping_config.json"
GOOGLE_MAPS_API_KEY = "API_GOES_HERE"
OUTPUT_FILE = "Output.html"
ROUTE_THRESHOLD = 750000
USE_THRESHOLD = True
WAYPOINTS_FILE = "my-waypoints-dist-dur.tsv"

START_POINT = "Las Vegas, NV";
END_POINT = "Nashville, TN";
MID_POINTS = [
                
                "Bryce Canyon National Park Visitor Center, Bryce, UT",
                "Chimayo, NM",
                "Albuquerque, NM",
                "Austin, TX",
                "Charlottesville, VA",
                "Vicksburg, MS",
                "Carlsbad Caverns Visitor Center, Carlsbad Cavern Highway, Carlsbad, NM",
                "San Antonio, TX",
                "Dallas, TX",
                "Tulsa, OK",
                "Memphis, TN",
                "Atlanta, GA",
                "Oklahoma City, OK",
                "New Orleans, LA",
                "Savannah, GA",
                "Charleston, SC",
                "Kitty Hawk, NC",
                "Oxford, MS",
                "Linville, NC",
                "Asheville, NC",
                "Richmond, VA",
                "Museum of the Cherokee Indian, 589 Tsali Boulevard, Cherokee, NC 28719",
                "Dollywood, 2700 Dollywood Parks Boulevard, Pigeon Forge, TN 37863",
                "Chattanooga, TN",
                "Indianola, MS",
                "Tupelo, MS",  # Natchez Trace Parkway Visitor Center
                "Fajada Butte View Point, Nageezi, NM 87037",
                "Black Canyon of the Gunnison National Park, Montrose, CO",
                "Chapin Mesa Archeological Museum, Mesa Verde National Park, CO",
                "Zion Lodge, 1 Zion Canyon Scenic Drive, Springdale, UT 84767",
                "North Rim Visitor Center, Grand Canyon National Park, Arizona 67, North Rim, AZ 86052",
                "Poverty Point State Historic Site, 6859 Louisiana 577, Pioneer, LA 71266",
                "Taos Pueblo, NM",
                "Silverton, CO",
                "Anasazi State Park Museum"
]

EXTRA_POINTS = [
"Flagstaff, AZ",
"Natural Bridges Rd, Lake Powell, UT 84533",
"Oljato-Monument Valley, UT",
"Omaha, NE",
"Little Rock, AR",
"Las Cruces, NM",
"Arches National Park Visitor Center & Park Headquarters, Arches Entrance Road, Utah",
"Great Sand Dunes Visitor Center, Mosca, CO",
"Terlingua, TX",
]

CAL_POINTS = [
            "Prairie Creek Visitor Center, California",  # Start Redwood Natl Park
            "Patrick's Point State Park, Patricks Point Drive, Trinidad, CA",  # End Redwood Natl Park     
            "Kohm Yah-mah-nee Visitor Center, 21820 Lassen National Park Hwy, Mineral, CA 96063, United States,",
            "Tahoe City, CA",        
            "Historic Mono Inn, 55620 US-395, Lee Vining, CA 93541, United States",  # Mono Lake
            "Yosemite Valley Visitor Center, 9035 Village Dr, Yosemite National Park, CA 95389",
            "Cedar Grove Visitor Center, North Side Drive, Kings Canyon National Park, CA 93633",
            "Manzanar, Manzanar Reward Rd, California",
            "Lodgepole Visitor Center, 63100 Lodgepole Road, Sequoia National Park, CA 93262",
            "Furnace Creek Inn, 328 Greenland Blvd., Death Valley, CA 92328"            
                
]



def get_api_key():
    with open(CONFIG_FILE) as data_file:    
        data = json.load(data_file)
        return data["GOOGLE_MAPS_API_KEY"]


def create_html_file(optimal_route, distance, display=1):
    optimal_route = list(optimal_route)

    print("")
    print("Shortest found: %d" % distance)
    print(optimal_route)                
    print("")

    Page_1 = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="initial-scale=1.0, user-scalable=no"><meta name="description" content="Randy Olson uses machine learning to find the optimal road trip across the U.S."><meta name="author" content="Randal S. Olson"><title>The optimal road trip across the U.S. according to machine learning</title><style>html, body, #map-canvas {height: 100%;margin: 0px;padding: 0px}#panel {position: absolute;top: 5px;left: 50%;margin-left: -180px;z-index: 5;background-color: #fff;padding: 10px;border: 1px solid #999;}</style><script src="https://maps.googleapis.com/maps/api/js?v=3.exp&signed_in=true"></script><script>var directionsDisplay1, directionsDisplay2;var directionsDisplay3, directionsDisplay4;var directionsDisplay5, directionsDisplay6;var markerOptions = {icon: "http://maps.gstatic.com/mapfiles/markers2/marker.png"};var directionsDisplayOptions = {preserveViewport: true,markerOptions: markerOptions};var directionsService = new google.maps.DirectionsService();var map;function initialize() {var center = new google.maps.LatLng(39, -96);var mapOptions = {zoom: 5,center: center};'
    Page_2 = "map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);directionsDisplay1.setMap(map);directionsDisplay2.setMap(map);directionsDisplay3.setMap(map);directionsDisplay4.setMap(map);directionsDisplay5.setMap(map);directionsDisplay6.setMap(map);}function calcRoute(start, end, routes) {switch (start) { "
    Page_3 = "}var waypts = [];for (var i = 0; i < routes.length; i++) {waypts.push({location:routes[i],stopover:true});}var request = {origin: start,destination: end,waypoints: waypts,optimizeWaypoints: false,travelMode: google.maps.TravelMode.DRIVING};directionsService.route(request, function(response, status) {if (status == google.maps.DirectionsStatus.OK) {switch (start) { "
    Page_4 = "}}});}google.maps.event.addDomListener(window, 'load', initialize); "
    Page_5 = '</script></head><body><div id="map-canvas"></div></body> '

    subset = 0
    subsetCounter = 0
    StatementC1 = ''
    StatementC2 = ''
    StatementCalcRoutes = ''

    while subset < len(optimal_route):
        subsetCounter += 1

        waypoint_subset = optimal_route[subset:subset + 10]
        output = "calcRoute(\"%s\", \"%s\", [" % (waypoint_subset[0], waypoint_subset[-1])
        StatementC1 = StatementC1 +  ' case "' + waypoint_subset[0] + '": directionsDisplay' + str(subsetCounter) + ' = new google.maps.DirectionsRenderer(directionsDisplayOptions); break; '
        StatementC2 = StatementC2 +  ' case "' + waypoint_subset[0] + '": directionsDisplay' + str(subsetCounter) + '.setDirections(response); break; '

        for waypoint in waypoint_subset[1:-1]:
            output += "\"%s\", " % (waypoint)
        
        if len(waypoint_subset[1:-1]) > 0:
            output = output[:-2]
        
        output += "]);"
        StatementCalcRoutes = StatementCalcRoutes + ' ' + output
        #print(output)
        #print("")
        subset += 9


    #write the output to file    
    localOUTPUT_FILE = OUTPUT_FILE.replace('.html', '_' + str(distance) + '.html')
    fs = open(localOUTPUT_FILE, 'w')
    fs.write(Page_1)
    fs.write(Page_2)
    fs.write(StatementC1)
    fs.write(Page_3)
    fs.write(StatementC2)
    fs.write(Page_4)
    fs.write(StatementCalcRoutes)
    fs.write(Page_5)
    fs.close()
    
    #Show the result
    if display ==1:
        webbrowser.open_new_tab(localOUTPUT_FILE)


def compute_fitness(solution):
    ''' returns the total duration traveled on the current road trip. '''

    solution_fitness = 0.0
    for index in range(len(solution)-1): # making it one-way
        waypoint1 = solution[index]
        waypoint2 = solution[index+1]
        solution_fitness += waypoint_durations[frozenset([waypoint1, waypoint2])]
        
    return solution_fitness


def mutate_route(agent_genome, max_mutations=3):
    """
        Applies 1 - `max_mutations` point mutations to the given road trip.
        
        A point mutation swaps the order of two waypoints in the road trip.
    """
    
    agent_genome = list(agent_genome)
    num_mutations = random.randint(1, max_mutations)
    
    for mutation in range(num_mutations):
        swap_index1 = random.randint(1, len(agent_genome) - 2) # protect first and last stops
        swap_index2 = swap_index1

        while swap_index1 == swap_index2:
            swap_index2 = random.randint(1, len(agent_genome) - 2)
        agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]
            
    return tuple(agent_genome)


def shuffle_route(agent_genome):
    """
        Applies a single shuffle mutation to the given road trip.
        
        A shuffle mutation takes a random sub-section of the road trip
        and moves it to another location in the road trip.
    """
    agent_genome = list(agent_genome)
    agent_genome = agent_genome[1:len(agent_genome)-1]
    
    start_index = random.randint(0, len(agent_genome) - 1)
    length = random.randint(2, 20)
    
    genome_subset = agent_genome[start_index:start_index + length]
    agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]
    
    insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
    agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

    agent_genome.insert(0, START_POINT)
    agent_genome.append(END_POINT)
    return tuple(agent_genome)


def generate_random_routes(number):    
    random_routes = []
    route_list = list(MID_POINTS)
    for agent in range(number):
        new_route = list(route_list)
        random.shuffle(new_route)
        new_route.insert(0, START_POINT)
        new_route.append(END_POINT)
        random_routes.append(tuple(new_route))
    return random_routes


def run_a_generation(population):
    route_fitness = {}
    for generation in range(4000):
        for route in population:
            if route in route_fitness:
                continue
            route_fitness[route] = compute_fitness(route)

        # Take the 20 shortest road trips and produce 20 offspring each from them
        new_population = []
        for rank, route in enumerate(sorted(route_fitness, key=route_fitness.get)[:15]):                   
            new_population.append(route)  # copy current route

            # Create 10 offspring with mutations
            for offspring in range(10):
                new_population.append(mutate_route(route, 5))
                
            # Create 9 offspring with a single shuffle mutation
            for offspring in range(9):
                new_population.append(shuffle_route(route))

        # Replace the old population with the new population of offspring 
        for i in range(len(population))[::-1]:
            del population[i]
        population = new_population
    best_result = sorted(route_fitness, key=route_fitness.get)[:1][0]
    return (best_result, route_fitness[best_result]) 


def run_genetic_algorithm():
    current_best_route = None
    current_best_route_len = -1
    if USE_THRESHOLD:
        current_best_route_len = ROUTE_THRESHOLD

    population = generate_random_routes(500)
    for generation in range(5):           
        (best_route, best_length) = run_a_generation(population)
        print("Best Route Found in Generation %d was %d") % (generation, best_length)
        if best_length < current_best_route_len:
            current_best_route = best_route
            current_best_route_len = best_length
            population = generate_random_routes(499)
            population.append(best_route)
            generation -= 1 #  keep going so long as keep finding better routes
        else:
            population = generate_random_routes(500)

    if current_best_route_len < ROUTE_THRESHOLD:
        return (current_best_route, current_best_route_len)
    else:
        print ("No better route found over threshold")
        return (None, None)


waypoint_distances = {}
waypoint_durations = {}
list_of_points = [] + MID_POINTS
list_of_points.append(START_POINT)
list_of_points.append(END_POINT)
all_waypoints = set()
for (waypoint1, waypoint2) in combinations(list_of_points, 2):
    temp_key = waypoint1 + '~' + waypoint2
    all_waypoints.add(temp_key)
    
print "Loading waypoints"
file_path = WAYPOINTS_FILE
if os.path.exists(file_path):
    waypoint_data = pd.read_csv(file_path, sep="\t")
    for i, row in waypoint_data.iterrows():
        waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
        waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
        temp_key = row.waypoint1 + '~' + row.waypoint2
        if temp_key in all_waypoints:
            all_waypoints.discard(temp_key)
        else: 
            temp_key = row.waypoint2 + '~' + row.waypoint1
            all_waypoints.discard(temp_key)  # already looked up
   
print "Collecting info on missing waypoints"
GOOGLE_MAPS_API_KEY = get_api_key()
gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
with open(WAYPOINTS_FILE, "a") as out_file:
    for path in all_waypoints:
        (waypoint1, waypoint2) = path.split('~')
        try:
            route = gmaps.distance_matrix(origins=[waypoint1],
                                          destinations=[waypoint2],
                                          mode="driving", # or "walking" or "bicycling", etc.
                                          language="English",
                                          units="metric")

            distance = route["rows"][0]["elements"][0]["distance"]["value"] # in meters
            duration = route["rows"][0]["elements"][0]["duration"]["value"] # in seconds

            waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
            waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

            out_file.write("\n" + "\t".join( [waypoint1, waypoint2, str(distance), str(duration)] ))

        except Exception as e:
            print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))
            print(e)

print "Optimizing route"
(optimal_route, route_length) = run_genetic_algorithm()
if optimal_route is not None:
    create_html_file(optimal_route, route_length)
