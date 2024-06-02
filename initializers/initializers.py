import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import object.vehicle as vehicle
import random
import initializers.init_node_positions as node
import initializers.init_edge_list as edge
import initializers.init_vehicle as vehi

def add_2jalur(a, b, we, wd):
	nodes = {
	'edge': (a, b),
	'weight': we,
	'width': wd}
	nodes2 = {
	'edge': (b, a),
	'weight': we,
	'width': wd}
	edge.edge_list.append(nodes)
	edge.edge_list.append(nodes2)
def add_jalur(a, b, we, wd):
	nodes = {
	'edge': (a, b),
	'weight': we,
	'width': wd}
	edge.edge_list.append(nodes)

def initEverything():
  # Initialize Pygame
	var.pyptr = pygame
	var.pyptr.init()
 
	# Initialize Screen
	var.width, var.height = 1200, 800
	screen.init_screen() 
	
	# Add more edges
	add_2jalur(7, 8, 1, 2)
	add_2jalur(7, 9, 1, 2)
	add_2jalur(7, 12, 1, 2)
	add_2jalur(12, 13, 1, 1)
	add_2jalur(12, 14, 1, 2)
	add_2jalur(14, 15, 1, 2)
	add_2jalur(14, 15, 1, 2)
	add_2jalur(15, 16, 1, 2)
	add_2jalur(15, 11, 1, 2)
	add_2jalur(9, 10, 1, 2)
	add_2jalur(9, 4, 1, 2)
	add_jalur(9, 11, 1, 2)
	add_jalur(11,9, 1, 1)
 
	# Set the minimum gap
	var.node_positions = {node: (pos[0] * var.minGap, pos[1] * var.minGap) for node, pos in node.init_node_positions.items()}
 
	# Remove edges that have nodes that are not in the node_positions
	currentLen = len(edge.edge_list)
	var.edge_list = [edge for edge in edge.edge_list if edge['edge'][0] in var.node_positions and edge['edge'][1] in var.node_positions]
 
	# Show warning when there are edges that are not in the node_positions
	if currentLen != len(var.edge_list):
		print('WARNING: Some edges are not in the node_positions')
	else:
		print('All edges are in the node_positions')
	
	# Create Graph
	visualizers.create_graph()

	# Main loop
 
	var.vehicles = []
 	# Create vehicles with initial positions
	for veh in vehi.initVehicle:
		# random the color
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		newVeh = vehicle.Vehicle((var.edgeWidth, var.edgeWidth), color, veh['type'], veh['begin'], veh['end'])
		if not newVeh.next_target == newVeh.position:
			var.vehicles.append(newVeh)