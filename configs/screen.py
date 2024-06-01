import configs.variables as var

def init_screen():
  # Set up display
	var.win = var.pyptr.display.set_mode((var.width, var.height))
	var.pyptr.display.set_caption("Graph Visualization with var.pyptr")