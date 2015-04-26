"""
Randy Olson's Shortest Route Program modified By Andrew Liesinger to:
    1: Detect waypoints file at runtime - if found use it, otherwise look up distances via google calls (and then save to waypoint file)
    2: Dynamically create and open an HTML file showing the route when a shorter route is found
    3: Make it easier to tinker with the Generation / Population parameters
"""
from itertools import combinations
import googlemaps
import pandas as pd
import numpy as np
import os.path
import random
import webbrowser

''' TODO: if waypoints exist, load those and look for new ones missing to cut down on API calls '''


waypoints_file = "my-waypoints-dist-dur.tsv"

#This is the general filename - as shorter routes are discovered the Population fitness score will be inserted into the filename
#so that interim results are saved for comparision.  The actual filenames using the default below will be:
#Output_<Population Fitness Score>.html 
output_file = 'Output.html'

#parameters for the Genetic algoritim
thisRunGenerations=25000
thisRunPopulation_size=500


start_point = "Seattle, WA";
end_point = "Seattle, WA";
mid_points = ["Flagstaff, AZ",
                "Page, AZ",
                "Olympia, WA",
                "Spokane, WA",
                "Thomas H. Kuchel Visitor Center, U.S. 101, Orick, CA",
                "Kohm Yah-mah-nee Visitor Center, 21820 Lassen National Park Hwy, Mineral, CA 96063, United States,",
                "Tahoe City, CA",
                "Historic Mono Inn, 55620 US-395, Lee Vining, CA 93541, United States",
                "Yosemite Valley Visitor Center, 9035 Village Dr, Yosemite National Park, CA 95389",
                "Cedar Grove Visitor Center, North Side Drive, Kings Canyon National Park, CA 93633",
                "Lodgepole Visitor Center, 63100 Lodgepole Road, Sequoia National Park, CA 93262",
                "Manzanar, Manzanar Reward Rd, California",
                "Furnace Creek Inn, 328 Greenland Blvd., Death Valley, CA 92328",
                "Las Vegas, NV",
                "Yakima, WA",
                "Glacier National Park",
                "Tillamook, OR",
                "Bandon, OR",
                "Teasdale, UT",
                "Arches National Park Visitor Center & Park Headquarters, Arches Entrance Road, Utah",
                "Bryce Canyon National Park Visitor Center, Bryce, UT",
                "Natural Bridges Rd, Lake Powell, UT 84533",
                "Oljato-Monument Valley, UT",
                "Silverton, CO",
                "Chambers, AZ",
                "Chimayo, NM",
                "Albuquerque, NM",
                "Austin, TX",
                "Charlottesville, VA",
                "Las Cruces, NM",
                "Vicksburg, MS",
                "Carlsbad, NM",
                "Terlingua, TX",
                "Lincoln, NE",
                "San Antonio, TX",
                "Dallas, TX",
                "Tulsa, OK",
                "Memphis, TN",
                "Atlanta, GA",
                "Lafayette, LA",
                "St. Louis, MO",
                "Oklahoma City, OK",
                "New Orleans, LA",
                "Savannah, GA",
                "Charleston, SC",
                "Linville, NC",
                "Asheville, NC",
                "Richmond, VA",
                "Museum of the Cherokee Indian, 589 Tsali Boulevard, Cherokee, NC 28719",
                "Dollywood, 2700 Dollywood Parks Boulevard, Pigeon Forge, TN 37863",
                "Nashville, TN",
                "Chattanooga, TN",
                "Kansas City, MO",
                "Omaha, NE",
                "Rapid City, SD",
                "Yellowstone National Park Visitor Center",
                "Mitchell Corn Palace, 604 North Main Street, Mitchell, SD 57301",
                "Little Rock, AR",
                "Indianola, MS",
                "Tupelo, MS",
                "Chinle, AZ",
                "Fajada Butte View Point, Nageezi, NM 87037",
                "Great Sand Dunes Visitor Center, Mosca, CO",
                "Black Canyon of the Gunnison National Park, Montrose, CO",
                "Co Road 7515, Bloomfield, NM 87413",
                "Chapin Mesa Archeological Museum, Mesa Verde National Park, CO",
                "C R 268A, Montezuma Creek, UT 84534",
                "Zion Lodge, 1 Zion Canyon Scenic Drive, Springdale, UT 84767",
                "Grand Canyon National Park"
]


def CreateOptimalRouteHtmlFile(optimal_route, distance, display=1):
    optimal_route = list(optimal_route)
    #optimal_route += [optimal_route[0]]


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
    localoutput_file = output_file.replace('.html', '_' + str(distance) + '.html')
    fs = open(localoutput_file, 'w')
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
        webbrowser.open_new_tab(localoutput_file)


def compute_fitness(solution):
    """ returns the total duration traveled on the current road trip."""

    solution_fitness = 0.0
    for index in range(len(solution)-1): # making it one-way
        waypoint1 = solution[index]
        waypoint2 = solution[index+1]
        #solution_fitness += waypoint_distances[frozenset([waypoint1, waypoint2])]
        solution_fitness += waypoint_durations[frozenset([waypoint1, waypoint2])]
        
    return solution_fitness

def generate_random_agent():
    """ Creates a random road trip from the waypoints. """ 
    new_random_agent = list(mid_points)
    random.shuffle(new_random_agent)
    new_random_agent.insert(0, start_point)
    new_random_agent.append(end_point)
    return tuple(new_random_agent)

def mutate_agent(agent_genome, max_mutations=3):
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

def shuffle_mutation(agent_genome):
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

    agent_genome.insert(0, start_point)
    agent_genome.append(end_point)
    return tuple(agent_genome)

def generate_random_population(pop_size):
    """
        Generates a list with `pop_size` number of random road trips.
    """
    
    random_population = []
    for agent in range(pop_size):
        random_population.append(generate_random_agent())
    return random_population
    
def run_genetic_algorithm(generations=5000, population_size=100):
    """
        The core of the Genetic Algorithm.
    """
    current_best_distance =-1
    # Create a random population of `population_size` number of solutions.
    population = generate_random_population(population_size)

    # For `generations` number of repetitions...
    for generation in range(generations):
        
        # Compute the fitness of the entire current population
        population_fitness = {}

        for agent_genome in population:
            if agent_genome in population_fitness:
                continue

            population_fitness[agent_genome] = compute_fitness(agent_genome)

        # Take the 10 shortest road trips and produce 10 offspring each from them
        new_population = []
        for rank, agent_genome in enumerate(sorted(population_fitness, key=population_fitness.get)[:10]):
            if (generation == generations - 1 and rank == 0):
                current_best_genome = agent_genome
                print("Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                       population_fitness[agent_genome],
                                                                       len(population_fitness)))
                print(agent_genome)                
                print("")
                    

            # Create 1 exact copy of each of the top 10 road trips
            new_population.append(agent_genome)

            # Create 2 offspring with 1-3 point mutations
            for offspring in range(2):
                new_population.append(mutate_agent(agent_genome, 3))
                
            # Create 7 offspring with a single shuffle mutation
            for offspring in range(7):
                new_population.append(shuffle_mutation(agent_genome))

        # Replace the old population with the new population of offspring 
        for i in range(len(population))[::-1]:
            del population[i]

        population = new_population
    return current_best_genome


waypoint_distances = {}
waypoint_durations = {}
list_of_points = [] + mid_points
list_of_points.append(start_point)
list_of_points.append(end_point)
all_waypoints = set()
import pdb
for (waypoint1, waypoint2) in combinations(list_of_points, 2):
    tempKey = waypoint1 + '~' + waypoint2
    all_waypoints.add(tempKey)
    
# if this file exists, read the data stored in it - if not then collect data by asking google
print "Begin finding shortest route"
file_path = waypoints_file
if os.path.exists(file_path):
    waypoint_data = pd.read_csv(file_path, sep="\t")
    for i, row in waypoint_data.iterrows():
        waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
        waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
        tempKey = row.waypoint1 + '~' + row.waypoint2
        if tempKey in all_waypoints:
            all_waypoints.discard(tempKey)
        else: 
            tempKey = row.waypoint2 + '~' + row.waypoint1
            all_waypoints.discard(tempKey)
   
print "Collecting Info on Missing Waypoints"
gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
with open(waypoints_file, "a") as out_file:
    for path in all_waypoints:
        (waypoint1, waypoint2) = path.split('~')
        try:
            route = gmaps.distance_matrix(origins=[waypoint1],
                                          destinations=[waypoint2],
                                          mode="driving", # or "walking" or "bicycling", etc.
                                          language="English",
                                          units="metric")

            distance = route["rows"][0]["elements"][0]["distance"]["value"] # in meters
            duration = route["rows"][0]["elements"][0]["duration"]["value"] #in seconds

            waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
            waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

            out_file.write("\n" + "\t".join( [waypoint1, waypoint2, str(distance), str(duration)] ))

        except Exception as e:
            print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))
            print(e)

print "Search for optimal route"
optimal_route = run_genetic_algorithm(generations=thisRunGenerations, population_size=thisRunPopulation_size)
CreateOptimalRouteHtmlFile(optimal_route, 1)
