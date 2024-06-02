import configs.variables as var
import nodes.visualizers as visualizers
import initializers.initializers as initializers
import probability.time as time
import probability.random as randomvar

def main(): 
	initializers.initEverything()
  
	loop = True
	while loop:
		visualizers.visualizeEverything()
		time.loop_time()
		randomvar.trigger_random()
		var.pyptr.display.flip()
		
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				loop = False

if __name__ == "__main__":
  main()