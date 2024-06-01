import configs.variables as var
import networkx as nx

def generate_shortest_path(source, target):
  return nx.dijkstra_path(var.G, source, target)

half_road = var.edgeWidth // 2

class Vehicle:
    def __init__(self, shape, color, start_position, final_target):
        # Find the position node location
        position = var.node_positions[start_position]
        self.x = position[0] - shape[0] // 2
        self.y = position[1] - shape[1] // 2
        self.dx = 0
        self.dy = 0
        self.width = shape[0]
        self.height = shape[1]
        self.color = color
        self.next_target = generate_shortest_path(start_position, final_target)[1]
        self.final_target = final_target
        self.speed = 0.5
    
    def goToTarget(self):
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
            self.next_target = generate_shortest_path(self.next_target, self.final_target)[1]
        pass

    def draw(self, screen):
        var.pyptr.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))