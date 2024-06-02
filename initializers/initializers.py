import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import object.vehicle as vehicle
import random
import initializers.init_node_positions as node
import initializers.init_edge_list as edge
import initializers.init_vehicle as vehi
import time
import probability.random as randomvar

def initEverything():
  # Initialize Pygame
	var.pyptr = pygame
	var.pyptr.init()
 
	# Initialize Screen
	var.width, var.height = 1200, 800
	screen.init_screen() 
 
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

	# Adjust Time
	var.last_updated = time.time()
 
	var.vehicles = []
 	# Create vehicles with initial positions
	for veh in vehi.initVehicle:
		# random the color
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		newVeh = vehicle.Vehicle((var.edgeWidth, var.edgeWidth), color, veh['type'], veh['begin'], veh['end'])
		if not newVeh.next_target == newVeh.position:
			var.vehicles.append(newVeh)
   
  # Initialize Repeaters
	randomvar.init_repeaters()