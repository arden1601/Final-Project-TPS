import configs.variables as var
import networkx as nx

def generate_shortest_path(source, target):
  return nx.dijkstra_path(var.G, source, target)

half_road = var.edgeWidth // 2
intolerance = var.edgeWidth // 3



class Vehicle:
  def __init__(self, shape, color, start_position, final_target):
    # Djikstra to find the next target
    try:
      self.next_target = generate_shortest_path(start_position, final_target)[1]
    except nx.NetworkXNoPath:
      self.next_target = start_position
    
    # Find the position node location
    spawn = var.node_positions[start_position]
    self.x = spawn[0] - shape[0] // 2
    self.y = spawn[1] - shape[1] // 2
    
    # Check if the vehicle is going horizontal or vertical
    self.position = start_position
    
    # Check the direction and action
    direction = self.direction()
    if direction == 'down':
      self.x += var.gap
    elif direction == 'up':
      self.x -= var.gap
    elif direction == 'right':
      self.y -= var.gap
    elif direction == 'left':
      self.y += var.gap
      
    # Check if the vehicle is spawned colliding with another vehicle
    while any(
      v.x - v.width // 2 < self.x + shape[0] + intolerance and
      v.x + v.width // 2 > self.x - intolerance and
      v.y - v.height // 2 < self.y + shape[1] + intolerance and
      v.y + v.height // 2 > self.y - intolerance
      for v in var.vehicles
    ):
      # Check if the next target requires a horizontal or vertical movement
      replacement = intolerance
      if var.node_positions[self.next_target][0] == var.node_positions[start_position][0]:
        # Vertical, move the vehicle the opposite direction
        if var.node_positions[self.next_target][1] > var.node_positions[start_position][1]:
          # Move up
          self.y -= replacement
        else:
          # Move down
          self.y += replacement
      else:
        # Horizontal, move the vehicle the opposite direction
        if var.node_positions[self.next_target][0] > var.node_positions[start_position][0]:
          # Move left
          self.x -= replacement
        else:
          # Move right
          self.x += replacement
    
    # Set the vehicle properties
    self.dx = 0
    self.dy = 0
    self.width = shape[0]
    self.height = shape[1]
    self.color = color
    car_img = var.pyptr.image.load('./assets/Audi.png')
    self.car = var.pyptr.transform.scale(car_img, (self.width, self.height))
      
    # add weight to the next target
    var.G[start_position][self.next_target]['weight'] = var.G[start_position][self.next_target]['weight'] + 1
    
    self.final_target = final_target
    self.speed = 0.5
  
  def goToTarget(self):
    # move the vehicle
    target = var.node_positions[self.next_target]
    
    # define the direction
    direction = self.direction()
    if direction == 'up':
      self.dx = 0
      self.dy = -1
    elif direction == 'down':
      self.dx = 0
      self.dy = 1
    elif direction == 'left':
      self.dx = -1
      self.dy = 0
    elif direction == 'right':
      self.dx = 1
      self.dy = 0
      
    # terminate the dx dy if the vehicle is close to the target with the changed coordinate based on previous direction
    def empty_dx_dy():
      self.dx = 0
      self.dy = 0
    
    if direction == 'up' and self.y == target[1] - var.gap // 2 - self.height:
      empty_dx_dy()
    elif direction == 'down' and self.y == target[1] - var.gap // 2 - self.height:
      empty_dx_dy()
    elif direction == 'left' and self.x == target[0] + var.gap // 2:
      empty_dx_dy()
    elif direction == 'right' and self.x == target[0] + var.gap // 2:
      empty_dx_dy()
    
    # # check if the next movement could collide with another vehicle
    next_x = self.x + self.dx * self.speed
    next_y = self.y + self.dy * self.speed

    # define 4 points of the vehicle
    top_left = (next_x - self.width // 2, next_y - self.height // 2)
    top_right = (next_x + self.width // 2, next_y - self.height // 2)
    bottom_left = (next_x - self.width // 2, next_y + self.height // 2)
    bottom_right = (next_x + self.width // 2, next_y + self.height // 2)

    # make sure the furthest border does not collide with another vehicle
    if any(
      v.x - v.width // 2 < max(top_left[0], top_right[0], bottom_left[0], bottom_right[0]) + intolerance and
      v.x + v.width // 2 > min(top_left[0], top_right[0], bottom_left[0], bottom_right[0]) - intolerance and
      v.y - v.height // 2 < max(top_left[1], top_right[1], bottom_left[1], bottom_right[1]) + intolerance and
      v.y + v.height // 2 > min(top_left[1], top_right[1], bottom_left[1], bottom_right[1]) - intolerance
      for v in var.vehicles if v != self
    ): 
      return
      
    # move the vehicle
    self.x += self.dx * self.speed
    self.y += self.dy * self.speed
    
    # check if the position is close to the target
    if self.dx == 0 and self.dy == 0:
      if not (self.next_target == self.final_target):
        # remove the previous weight
        var.G[self.position][self.next_target]['weight'] = var.G[self.position][self.next_target]['weight'] - 1
        
        # Switch to the next target
        self.position = self.next_target
        self.next_target = generate_shortest_path(self.next_target, self.final_target)[1]
        
        # add weight to the next target if it is not the final target
        var.G[self.position][self.next_target]['weight'] = var.G[self.position][self.next_target]['weight'] + 1
      else:
        # remove the previous weight
        var.G[self.position][self.next_target]['weight'] = var.G[self.position][self.next_target]['weight'] - 1
        
        # remove the vehicle
        var.vehicles.remove(self)

  def direction(self):
    if var.node_positions[self.next_target][0] == var.node_positions[self.position][0]:
      # Vertical
      # Check if the target vector is to the top or bottom
      if var.node_positions[self.next_target][1] > var.node_positions[self.position][1]: # Vector to the bottom
        return 'down'
      else: # Vector to the top
        return 'up'
    else:
      # Horizontal
      # Check if the target vector is to the left or right
      if var.node_positions[self.next_target][0] > var.node_positions[self.position][0]: # Vector to the right
        return 'right'
      else: # Vector to the left
        return 'left'

  def draw(self, screen):
    # Check if the vehicle coordinate is out of the screen
    if self.x < -self.width or self.x > var.width or self.y < -self.height or self.y > var.height:
      return
    
    var.pyptr.draw.rect(screen, self.color, (self.x + var.viewMargin[0], self.y + var.viewMargin[1], self.width, self.height))