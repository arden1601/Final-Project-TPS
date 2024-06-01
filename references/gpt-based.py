import pygame
import networkx as nx

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graph Visualization with Pygame")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define node positions
node_positions = {
    1: (100, 100),
    2: (200, 200),
    3: (300, 100),
    4: (400, 300),
}

# Create a graph
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])

def draw_graph():
    win.fill(WHITE)
    
    # Draw edges
    for edge in G.edges():
        start_pos = node_positions[edge[0]]
        end_pos = node_positions[edge[1]]
        pygame.draw.line(win, BLACK, start_pos, end_pos, 2)
    
    # Draw nodes
    for node, pos in node_positions.items():
        pygame.draw.circle(win, BLUE, pos, 20)
        font = pygame.font.Font(None, 24)
        text = font.render(str(node), True, WHITE)
        win.blit(text, (pos[0] - 5, pos[1] - 8))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_graph()
    pygame.display.flip()

pygame.quit()
