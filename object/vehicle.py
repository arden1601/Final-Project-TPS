import configs.variables as var
import networkx as nx
import configs.extras as extras
import time

half_road = var.edgeWidth // 2
intolerance = var.edgeWidth // 3

class Vehicle:
  def __init__(self, shape, color, type, start_position, final_target):
    self.start_time = time.time() 
    self.time_taken = 0
    # Djikstra to find the next target
    self.type = type
    try:
      self.next_target = extras.generate_shortest_path(start_position, final_target, extras.generate_width_required(self.type))[1]
    except (nx.NetworkXNoPath, nx.NodeNotFound):
      self.next_target = start_position
    except IndexError:
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
    self.showWidth = self.width
    self.showHeight = self.height
    self.color = color
    self.veh_img = None
    self.gonnaOccupied = False
    self.insideOccupied = False
    
    try:
      # iterate through the veh_options
      for veh_option in var.veh_choices:
        # check if the vehicle type is in the veh_options
        if self.type == veh_option['name']:
          # load the image
          self.veh_img = var.pyptr.image.load(veh_option['img'])
          break
      
    except:
      print('Error loading the vehicle image')
    
    self.veh = var.pyptr.transform.scale(self.veh_img, (self.width , self.height))
      
    # add weight to the next target only if the next target is not the current target
    if not (self.next_target == self.position):
      var.G[0]['graph'][start_position][self.next_target]['weight'] = var.G[0]['graph'][start_position][self.next_target]['weight'] + 1
    
    self.final_target = final_target
    self.speed = 1 if self.type == 'car' else 2
  
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
    positionHandler = self.height
    
    if direction == 'up' and self.y == target[1] - var.gap // 2 - positionHandler * multiplier:
      empty_dx_dy()
    elif direction == 'down' and self.y == target[1] - var.gap // 2 + positionHandler * multiplier:
      empty_dx_dy()
    elif direction == 'left' and self.x == target[0] - var.gap // 2 - positionHandler * multiplier:
      empty_dx_dy()
    elif direction == 'right' and self.x == target[0] - var.gap // 2 + positionHandler * multiplier:
      empty_dx_dy()
  
    # check if the next movement could collide with another vehicle
    next_x = self.x + self.dx * self.speed
    next_y = self.y + self.dy * self.speed

    coor_x = next_x + var.viewMargin[0]
    coor_y = next_y + var.viewMargin[1]

    # define 4 points of the current vehicle in the next movement
    top_left = (coor_x, coor_y)
    top_right = (coor_x + self.showWidth, coor_y)
    bottom_left = (coor_x, coor_y + self.showHeight)
    bottom_right = (coor_x + self.showWidth, coor_y + self.showHeight)
    
    # draw box around the vehicle
    if var.show_node_boxes:
      # get the config of the current vehicle type
      opt = None
      for veh_option in var.veh_choices:
        if self.type == veh_option['name']:
          opt = veh_option
          break
      
      # revert direction handler
      if not self.reverting:
        self.showWidth = self.width * opt['w-scale']
        self.showHeight = self.height * opt['h-scale']
        
        dir = self.direction()
        if dir == 'up' or dir == 'down':
          self.showWidth, self.showHeight = self.showHeight, self.showWidth
      
      var.pyptr.draw.rect(
        var.win,
        var.colors['GREEN'],
        var.pyptr.Rect(
          top_left[0],
          top_left[1],
          self.showWidth,
          self.showHeight
        ),
        2
      )
      
    # check if the vehicle is going to hit busy nodes
    self.gonnaOccupied = False
    self.insideOccupied = False
    for occupy in var.node_occupy:
      node = occupy['node']
      
      # get the node position
      pos = var.node_positions[node]
      
      occupy_addr = None
      # Find the node in node_occupy
      for addr in var.node_occupy:
        if addr['node'] == node:
          occupy_addr = addr
          break
      
      if occupy_addr == None:
        break
      
      # check if the vehicle is currently inside the node
      # real 4 current position
      top_left_real = (self.x, self.y)
      top_right_real = (self.x + self.showWidth, self.y)
      bottom_left_real = (self.x, self.y + self.showHeight)
      
      # check if the vehicle is going to hit the node
      if (
        # use real position
        top_left_real[0] < pos[0] + var.viewMargin[0] + var.edgeWidth*1.4 and
        pos[0] + var.viewMargin[0] - var.edgeWidth*1.4 < top_right_real[0] and
        top_left_real[1] < pos[1] + var.viewMargin[1] + var.edgeWidth*1.4 and
        pos[1] + var.viewMargin[1] - var.edgeWidth*1.4 < bottom_left_real[1]
      ):
        self.insideOccupied = True
      
      # check if the vehicle is going to hit the node
      if (
        top_left[0] < pos[0] + var.viewMargin[0] + var.edgeWidth*1.4 and
        pos[0] + var.viewMargin[0] - var.edgeWidth*1.4 < top_right[0] and
        top_left[1] < pos[1] + var.viewMargin[1] + var.edgeWidth*1.4 and
        pos[1] + var.viewMargin[1] - var.edgeWidth*1.4 < bottom_left[1]
      ):
        self.gonnaOccupied = True
        
        # Check if the vehicle is standing on a node that assigned to itself
        if occupy_addr['vehicle'] == self:
          # print('Vehicle is going to stand on a node that assigned to itself')
          pass
        else:
          # print('Vehicle is going to stand on a node that assigned to another vehicle')
          return
    
    # if the vehicle is not going to hit the busy nodes, remove the vehicle from the node_occupy
    if not self.gonnaOccupied:
      self.clearOccupation()
    
    # check if the vehicle is going to hit another vehicle
    for v in var.vehicles:
      if v == self:
        continue
      
      # define 4 points of the vehicle compared
      coor_x = v.x + var.viewMargin[0]
      coor_y = v.y + var.viewMargin[1]
      top_left_v = (coor_x, coor_y)
      top_right_v = (coor_x + v.showWidth, coor_y)
      bottom_left_v = (coor_x, coor_y + v.showHeight)
      bottom_right_v = (coor_x + v.showWidth, coor_y + v.showHeight)
      
      # check if the vehicle is going to hit another vehicle based on the direction, use top_left_v, top_right_v, bottom_left_v, bottom_right_v
      myDir = self.direction()
      
      # ensure if the vehicle is facing to front, check only the back side of the vehicle,
      oppInBack = (
        (myDir == 'up' and (
          top_left[1] < bottom_left_v[1] and
          top_right[1] < bottom_right_v[1] and
          top_left[0] < bottom_right_v[0] and
          top_right[0] > bottom_left_v[0]          
        )) or
        (myDir == 'down' and (
          bottom_left[1] > top_left_v[1] and
          bottom_right[1] > top_right_v[1] and
          bottom_left[0] < top_right_v[0] and
          bottom_right[0] > top_left_v[0]
        )) or
        (myDir == 'left' and (
          top_left[0] < top_right_v[0] and
          bottom_left[0] < bottom_right_v[0] and
          top_left[1] < bottom_right_v[1] and
          bottom_left[1] > top_right_v[1]
        )) or
        (myDir == 'right' and (
          top_right[0] > top_left_v[0] and
          bottom_right[0] > bottom_left_v[0] and
          top_right[1] < bottom_left_v[1] and
          bottom_right[1] > top_left_v[1]
        ))
      )
      
      # distance between the vehicle
      distance = 0
      if myDir == 'up':
        distance = top_left_v[1] - top_left[1]
      elif myDir == 'down':
        distance = top_left[1] - top_left_v[1]
      elif myDir == 'left':
        distance = top_left_v[0] - top_left[0]
      elif myDir == 'right':
        distance = top_left[0] - top_left_v[0]
      
      # handle if the next step of current vehicle is going to hit another vehicle
      if (not oppInBack) and (
        top_left[0] < top_right_v[0] and
        top_right[0] > top_left_v[0] and
        top_left[1] < bottom_right_v[1] and
        bottom_left[1] > top_right_v[1]
      ):
        # if the vehicle is inside a busy node, ignore the collision
        if self.insideOccupied:
          continue
        
        return
      
      # handle if the other vehicle is in the back of the current vehicle
      if oppInBack:
        if distance < intolerance and self.direction() == v.direction():
          # draw YELLOW box around the vehicle that causes self to stop
          if var.show_node_boxes:
            var.pyptr.draw.rect(
              var.win,
              var.colors['YELLOW'],
              var.pyptr.Rect(
                top_left_v[0],
                top_left_v[1],
                v.showWidth,
                v.showHeight
              ),
              2
            )
            
          # draw BLUE box around the vehicle that is going to stop
          if var.show_node_boxes:
            var.pyptr.draw.rect(
              var.win,
              var.colors['BLUE'],
              var.pyptr.Rect(
                top_left[0],
                top_left[1],
                self.showWidth,
                self.showHeight
              ),
              2
            )
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
        end_time = time.time()
        self.time_taken = (end_time - self.start_time)/2 if self.type == 'bike' else (end_time - self.start_time) 
        var.time_taken.append(self.time_taken)
        
        # remove the vehicle from the node_occupy
        self.clearOccupation()
        
        
        
        # recount the quota
        extras.recount_quota()

  def clearOccupation(self):
    for addr in var.node_occupy:
        if addr['vehicle'] == self:
          var.node_occupy.remove(addr)

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
    props = None
    for veh_option in var.veh_choices:
      if self.type == veh_option['name']:
        props = veh_option
        break
    
    if self.veh_direction == 'down':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.height * props['w-scale']  , self.width * props['w-scale']))
      rotate_image = var.pyptr.transform.rotate(self.veh, 180)
      self.veh = rotate_image
    elif self.veh_direction == 'left':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.width  * props['w-scale'], self.height * props['w-scale']))
      rotate_image = var.pyptr.transform.rotate(self.veh, 90)
      self.veh = rotate_image
    elif self.veh_direction == 'right':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.width  * props['w-scale'], self.height * props['w-scale']))
      rotate_image = var.pyptr.transform.rotate(self.veh, 270)
      self.veh = rotate_image
    elif self.veh_direction == 'up':
      self.veh = var.pyptr.transform.scale(self.veh_img, (self.height * props['w-scale'] , self.width * props['w-scale']))

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
      
    # find the object config from the vehicle options
    opt = None
    for veh_option in var.veh_choices:
      if self.type == veh_option['name']:
        opt = veh_option
        break
    
    draw_hori = self.x + var.viewMargin[0] - (self.width * opt['w-scale'] - var.edgeWidth) // 2
    draw_vert = self.y + var.viewMargin[1] - (self.width * opt['w-scale'] - var.edgeWidth) // 2
    
    if self.type == 'car':
      if self.veh_direction == 'down':
        screen.blit(self.veh, (draw_hori , draw_vert + 20 ))
      elif self.veh_direction == 'right':
        screen.blit(self.veh, (draw_hori + 20 , draw_vert ))
      elif self.veh_direction == 'left':
        screen.blit(self.veh, (draw_hori + 20 , draw_vert  ))
      elif self.veh_direction == 'up':
        screen.blit(self.veh, (draw_hori , draw_vert + 20  ))
    else:
      screen.blit(self.veh, (draw_hori , draw_vert ))
      
        