# import packages
import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers

def main(): 
	# Initialize Pygame
	var.pyptr = pygame
	var.pyptr.init()
 
	# Initialize Screen
	var.width, var.height = 600, 500
	screen.init_screen() 
 
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