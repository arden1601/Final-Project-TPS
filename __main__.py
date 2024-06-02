# import packages
import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import object.vehicle as vehicle
import random
import configs.init_node_positions as node
import configs.init_edge_list as edge

def main(): 
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

	# Main loop
	initVehicle = [
   {
		'begin': 1,
		'end': 14,
		'type': 'bike'
	 },{
		'begin': 1,
		'end': 14,
		'type': 'bike'
	 },{
		'begin': 1,
		'end': 14,
		'type': 'car'
	 },]
	# },
	# {
	# 	'begin': 1,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
	# {
	# 	'begin': 1,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
 	# {
	# 	'begin': 2,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
	# {
	# 	'begin': 2,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
	# {
	# 	'begin': 2,
	# 	'end': 8,
	# 	'type': 'bike'
	# }]
 
	var.vehicles = []
 	# Create vehicles with initial positions
	for veh in initVehicle:
		# random the color
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		newVeh = vehicle.Vehicle((var.edgeWidth, var.edgeWidth), color, veh['type'], veh['begin'], veh['end'])
		if not newVeh.next_target == newVeh.position:
			var.vehicles.append(newVeh)
   
	running = True
	while running:
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				running = False

		visualizers.draw_graph()	
		# visualizers.draw_the_road()
		visualizers.draw_vehicles()
  
		visualizers.draw_vehicles()
		var.pyptr.display.flip()

if __name__ == "__main__":
  main()