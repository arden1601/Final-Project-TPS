import configs.variables as var
import networkx as nx

def generate_shortest_path(source, target):
  return nx.dijkstra_path(var.G, source, target)

half_road = var.edgeWidth // 2

class Vehicle:
    def __init__(self, start_position, shape, color, final_target):
        # Find the position node location
        position = var.node_positions[start_position]
        self.x = position[0]
        self.y = position[1]
        self.width = shape[0]
        self.height = shape[1]
        self.color = color
        self.next_target = generate_shortest_path(1, final_target)[1]
        self.final_target = final_target
        self.speed = 0.5
    
    def goToTarget(self):
        target = var.node_positions[self.next_target]
        dx = target[0] - self.x - half_road
        dy = target[1] - self.y - half_road
        
        if dx != 0:
          dx = dx / abs(dx)
        elif dy != 0:
          dy = dy / abs(dy)
          
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # check if the position is close to the target
        if dx == 0 and dy == 0:
          if not (self.next_target == self.final_target):
            self.next_target = generate_shortest_path(self.next_target, self.final_target)[1]

    def draw(self, screen):
        var.pyptr.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))