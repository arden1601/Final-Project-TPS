# Showing what in weights?
show_opt = ['quota', 'vehicles', 'weight']
show = show_opt[-1]

# Show the boxes to vehicles?
show_boxes = True

# Show the busy nodes?
show_busy = True

# Show the road?
show_road = True

# Show node boxes?
show_node_boxes = False

# Show the clock
show_clock = True

# Show the vehicles count?
show_vehicle_count = True

# Screen Properties
width, height = 0, 0
win = None

# Clock
clock_limit = 24
clock_min_limit = 4
clock = 4
clock_min = 0
last_updated = 0
delay = 1
repeater = []

# Lib
pyptr = None

# Nodes
minGap = 100
edgeWidth = 20
gap = edgeWidth * .9
G = []
viewMargin = (50, 50)
node_positions = {}
edge_list = []
busy_node = []
node_occupy = []

def getEdgeLength(start, stop):
  target_edge = (start, stop)
  
  # Initialize a variable to hold the found edge
  found_edge = None

  # Iterate over the edge list
  for edge_info in edge_list:
    if edge_info['edge'] == target_edge:
      found_edge = edge_info
      break
    
  # extract the start and stop node positions
  nodes = found_edge['edge']
  start_node = node_positions[nodes[0]]
  stop_node = node_positions[nodes[1]]
  
  # get the distance between the nodes
  x = abs(start_node[0] - stop_node[0])
  y = abs(start_node[1] - stop_node[1])
  
  # measure the distance between the nodes using pythagorean theorem
  distance = (x**2 + y**2)**.5
  
  # return the distance
  return distance / minGap * 2

# Vehicles
vehicles = []
gigaNumber = 999999
max_vehicles = 30
veh_choices = [
  {
    'name': 'bike',
    'width': 1,
    'img': './assets/bike.png',
    'w-scale': 1,
    'h-scale': 1
  },
  {
    'name': 'car',
    'width': 2,
    'img': './assets/car.png',
    'w-scale': 3,
    'h-scale': 1
  }
]

# Average Time
time_taken = []
# Colors
colors = {
  'WHITE': (255, 255, 255),
  'BLACK': (0, 0, 0),
  'BLUE': (0, 0, 255),
  'RED': (255, 0, 0),
  'GREEN': (0, 255, 0),
  'GRAY': (127, 127, 127),
  'YELLOW': (255, 255, 0),
}

# Visualizers
howManyStats = 0
statsGap = 15