import random
import time
import object.vehicle as vehicle
import configs.variables as var
import networkx as nx
import configs.extras as extras

def add_repeater(name, repeating, start, end, action):
  var.repeater.append({
    'name': name,
    'delay': repeating,
    'onInterval': (start, end),
    'lastTime': time.time(),
    'action': action,
  })

def init_repater_vehicle():
  add_repeater('random_vehicle', .01, 0, 24, random_vehicle)

def random_vehicle():
  # check if the vehicle is full
  if len(var.vehicles) >= var.max_vehicles:
    return
  
  # get biggest node value
  max_node = max(var.node_positions.keys())
  
  # random type
  random_type = random.choice([veh['name'] for veh in var.veh_choices])
  
  nodes_start = [1,2,5,8,10,13,16]
  while True:
    # random begin
    busy_node = [node['node'] for node in var.node_occupy]
    
    random_begin = random.choice(nodes_start)  if len(var.node_occupy) == 0 else random.choice(busy_node)
    while random_begin in busy_node:
      random_begin = random.randint(1, max_node) 
    
    # random end not equal to random begin
    random_end = random_begin
    while random_end == random_begin:
      random_end = random.randint(1, max_node)
      
    # Make sure the path is possible
    try:
      extras.generate_shortest_path(random_begin, random_end, extras.generate_width_required(random_type))
    except (nx.NetworkXNoPath, nx.NodeNotFound):
      continue
    break
  
  # create a random vehicle
  veh = {
    'begin': random_begin,
    'end': 11,
    'type': random_type
  }
  
  # random the color
  color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
  
  newVeh = vehicle.Vehicle((var.edgeWidth, var.edgeWidth), color, veh['type'], veh['begin'], veh['end'])
  if not newVeh.next_target == newVeh.position:
    var.vehicles.append(newVeh)

def init_repeaters():
  init_repater_vehicle()

def trigger_random():
  for repeater in var.repeater:
    if time.time() - repeater['lastTime'] > repeater['delay'] and var.clock >= repeater['onInterval'][0] and var.clock <= repeater['onInterval'][1]: 
      repeater['action']()
      repeater['lastTime'] = time.time()