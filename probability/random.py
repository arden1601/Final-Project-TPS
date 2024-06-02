import random
import time
import object.vehicle as vehicle
import configs.variables as var

def add_repeater(name, repeating, start, end, action):
  var.repeater.append({
    'name': name,
    'delay': repeating,
    'onInterval': (start, end),
    'lastTime': time.time(),
    'action': lambda: action
  })
  

def init_repater_vehicle():
  add_repeater('random_vehicle', 1, 0, 24, random_vehicle)

def random_vehicle():
  # get biggest node value
  max_node = max(var.node_positions.keys())
  
  # random begin
  random_begin = random.randint(1, max_node)
  
  # random end not equal to random begin
  random_end = random_begin
  while random_end == random_begin:
    random_end = random.randint(1, max_node)
  
  # random type
  random_type = random.choice(['car', 'bike'])
  
  # create a random vehicle
  veh = {
    'begin': random_begin,
    'end': random_end,
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
    if repeater['name'] == 'random_vehicle':
      if time.time() - repeater['lastTime'] > repeater['delay'] and var.clock >= repeater['onInterval'][0] and var.clock <= repeater['onInterval'][1]:
        random_vehicle()
        repeater['lastTime'] = time.time()