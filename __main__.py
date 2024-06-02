import configs.variables as var
import nodes.visualizers as visualizers
import initializers.initializers as initializers
import probability.time as time
import probability.random as randomvar
import configs.extras as extras

def main(): 
	initializers.initEverything()
  
	loop = True
	while loop:
		visualizers.visualizeEverything()
		time.loop_time()
		randomvar.trigger_random()
		extras.check_nodes_contain_vehicle()
  
  
		var.pyptr.display.flip()
		
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				loop = False

if __name__ == "__main__":
  main()