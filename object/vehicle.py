import configs.variables as var
import networkx as nx
import configs.extras as extras

half_road = var.edgeWidth // 2
intolerance = var.edgeWidth // 3

class Vehicle:
  def __init__(self, shape, color, type, start_position, final_target):
    # Djikstra to find the next target
    self.type = type
    try:
      print(start_position, final_target)
      self.next_target = extras.generate_shortest_path(start_position, final_target, extras.generate_width_required(self.type))[1]
    except nx.NetworkXNoPath:
      self.next_target = start_position
    
    # Find the position node location
    spawn = var.node_positions[start_position]
    self.x = spawn[0] - shape[0] // 2
    self.y = spawn[1] - shape[1] // 2
    
    # Check if the vehicle is going horizontal or vertical
    self.position = start_position
    self.incoming = self.direction()
    self.prevIncoming = None
    self.reverting = False
    
    # Check the direction and action
    self.veh_direction = ''
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
    
    try:
      if self.type == 'bike':
        self.veh_img = var.pyptr.image.load('./assets/bike.png')
      elif self.type == 'car':
        self.veh_img = var.pyptr.image.load('./assets/car.png')
    except:
      print('Error loading the vehicle image')
    self.veh = var.pyptr.transform.scale(self.veh_img, (self.width , self.height))
      
    # add weight to the next target only if the next target is not the current target
    if not (self.next_target == self.position):
      var.G[0]['graph'][start_position][self.next_target]['weight'] = var.G[0]['graph'][start_position][self.next_target]['weight'] + 1
    
    self.final_target = final_target
    self.speed = .5
  
  def goToTarget(self):
    # Target direction
    target = var.node_positions[self.next_target]
    
    # ignore if the vehicle's position is the same as the target
    if self.position == self.next_target:
      return
    
    # define the direction
    direction = self.incoming if not self.reverting else self.prevIncoming
    self.movDir(direction)
    
    # terminate the dx dy if the vehicle is close to the target with the changed coordinate based on previous direction
    def empty_dx_dy():
      self.dx = 0
      self.dy = 0
      self.reverting = False
    
    # revert handler
    prevRevert = self.reverting
    multiplier = -1 if not self.reverting else 1
    if direction == 'up' and self.y == target[1] - var.gap // 2 - self.height * multiplier:
      empty_dx_dy()
    elif direction == 'down' and self.y == target[1] - var.gap // 2 + self.height * multiplier:
      empty_dx_dy()
    elif direction == 'left' and self.x == target[0] - var.gap // 2 - self.width * multiplier:
      empty_dx_dy()
    elif direction == 'right' and self.x == target[0] - var.gap // 2 + self.width * multiplier:
      empty_dx_dy()
  
    # check if the next movement could collide with another vehicle
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
      
    # check if the next movement exceeds the target
    if direction == 'up' and next_y < target[1] - var.gap // 2 - self.height * multiplier:
      self.y = target[1] - var.gap // 2 - self.height * multiplier
      empty_dx_dy()
    elif direction == 'down' and next_y > target[1] - var.gap // 2 + self.height * multiplier:
      self.y = target[1] - var.gap // 2 + self.height * multiplier
      empty_dx_dy()
    elif direction == 'left' and next_x < target[0] - var.gap // 2 - self.width * multiplier:
      self.x = target[0] - var.gap // 2 - self.width * multiplier
      empty_dx_dy()
    elif direction == 'right' and next_x > target[0] - var.gap // 2 + self.width * multiplier:
      self.x = target[0] - var.gap // 2 + self.width * multiplier
      empty_dx_dy()
      
    # move the vehicle
    self.x += self.dx * self.speed
    self.y += self.dy * self.speed
    
    # check if the position is close to the target
    if self.dx == 0 and self.dy == 0:
      extras.recount_quota()
      
      if prevRevert:
        return
        
      if not (self.next_target == self.final_target):
        # remove the previous weight
        var.G[0]['graph'][self.position][self.next_target]['weight'] = var.G[0]['graph'][self.position][self.next_target]['weight'] - 1
        
        # Switch to the next target
        self.prevIncoming = self.incoming
        self.position = self.next_target
        self.next_target = extras.generate_shortest_path(self.next_target, self.final_target, extras.generate_width_required(self.type))[1]
        
        # Reset the direction
        self.incoming = self.direction()
        if self.revertLine():
          self.reverting = True  
        
        # add weight to the next target if it is not the final target
        var.G[0]['graph'][self.position][self.next_target]['weight'] = var.G[0]['graph'][self.position][self.next_target]['weight'] + 1

      else:
        # remove the previous weight
        var.G[0]['graph'][self.position][self.next_target]['weight'] = var.G[0]['graph'][self.position][self.next_target]['weight'] - 1
        
        # remove the vehicle
        var.vehicles.remove(self)
        
        # recount the quota
        extras.recount_quota()

  def movDir(self, direction):
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

  def direction(self):
    if var.node_positions[self.next_target][0] == var.node_positions[self.position][0]:
      # Vertical
      # Check if the target vector is to the top or bottom
      if var.node_positions[self.next_target][1] > var.node_positions[self.position][1]: # Vector to the bottom
        self.veh_direction = 'down'
        return 'down'
      else: # Vector to the top
        self.veh_direction = 'up'
        return 'up'
    else:
      # Horizontal
      # Check if the target vector is to the left or right
      if var.node_positions[self.next_target][0] > var.node_positions[self.position][0]: # Vector to the right
        self.veh_direction = 'right'
        return 'right'
      else: # Vector to the left
        self.veh_direction = 'left'
        return 'left'
      
  def handle_direction(self):
    if self.veh_direction == 'down':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.width , self.height))
      rotate_image = var.pyptr.transform.rotate(self.veh, 180)
      self.veh = rotate_image
    elif self.veh_direction == 'left':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.width , self.height))
      rotate_image = var.pyptr.transform.rotate(self.veh, 90)
      self.veh = rotate_image
    elif self.veh_direction == 'right':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.width , self.height))
      rotate_image = var.pyptr.transform.rotate(self.veh, 270)
      self.veh = rotate_image
    else:
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.width , self.height))

  def revertLine(self):
    # Check if the vehicle is going horizontal or vertical
    prevDir = self.prevIncoming
    direction = self.incoming
    doRevert = False
    if prevDir == 'down':
      if direction == 'up' or direction == 'left':
        doRevert = True
    elif prevDir == 'up':
      if direction == 'down' or direction == 'right':
        doRevert = True
    elif prevDir == 'right':
      if direction == 'left' or direction == 'down':
        doRevert = True
    elif prevDir == 'left':
      if direction == 'right' or direction == 'up':
        doRevert = True
        
    return doRevert

  def draw(self, screen):
    # Check if the vehicle coordinate is out of the screen
    if self.x < -self.width or self.x > var.width or self.y < -self.height or self.y > var.height:
      return
    
    if not self.reverting:
      self.handle_direction()
    
    screen.blit(self.veh, (self.x + var.viewMargin[0], self.y + var.viewMargin[1]))