import configs.variables as var

def init_screen():
  # Set up display
	var.win = var.pyptr.display.set_mode((var.width, var.height))
 
 	# Set up title
	var.pyptr.display.set_caption("Shortest Path Visualizer")