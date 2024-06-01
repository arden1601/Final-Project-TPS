# import packages
import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import nodes.vert_edge as vert_edge

def main(): 
	# Initialize Pygame
	var.pyptr = pygame
	var.pyptr.init()
 
	# Initialize Screen
	var.width, var.height = 1000, 600
	screen.init_screen() 
 
	# Initialize Nodes and Edges
  # Parameters
	total_vertices = 30
	total_edges = 40
	x_range = (200, 800)
	y_range = (100, 500)
	weight_range = (1, 10)

	# Generate random vertices and edges
	var.node_positions = vert_edge.generate_random_vertices(total_vertices, x_range, y_range, var.node_positions)
	var.edge_list = vert_edge.generate_random_edges(total_edges, total_vertices, weight_range, var.edge_list)
 
	# Create Graph
	visualizers.create_graph()

	# Main loop
	running = True
	while running:
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				running = False

		visualizers.draw_graph()
		var.pyptr.display.flip()
  
	var.pyptr.quit()

if __name__ == "__main__":
  main()