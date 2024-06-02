import configs.variables as var
import networkx as nx

def generate_shortest_path(source, target):
  return nx.dijkstra_path(var.G, source, target)

half_road = var.edgeWidth // 2
intolerance = var.edgeWidth // 3

class Vehicle:
  def __init__(self, shape, color, start_position, final_target):
    # Find the position node location
    spawn = var.node_positions[start_position]
    self.x = spawn[0] - shape[0] // 2
    self.y = spawn[1] - shape[1] // 2
    self.position = start_position
    self.dx = 0
    self.dy = 0
    self.width = shape[0]
    self.height = shape[1]
    self.color = color
    try:
      self.next_target = generate_shortest_path(start_position, final_target)[1]
    except nx.NetworkXNoPath:
      # Kill the vehicle if there is no path
      var.vehicles.remove(self)
    # add weight to the next target
    var.G[start_position][self.next_target]['weight'] = var.G[start_position][self.next_target]['weight'] + 1
    
    self.final_target = final_target
    self.speed = 0.5
  
  def goToTarget(self):
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
  
    # move the vehicle
    target = var.node_positions[self.next_target]
    self.dx = target[0] - self.x - half_road
    self.dy = target[1] - self.y - half_road
    
    if self.dx != 0:
      self.dx = self.dx / abs(self.dx)
    elif self.dy != 0:
      self.dy = self.dy / abs(self.dy)
      
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

  def draw(self, screen):
    var.pyptr.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))