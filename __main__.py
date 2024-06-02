import configs.variables as var
import nodes.visualizers as visualizers
import initializers.initializers as initializers

def main(): 
	initializers.initEverything()
  
	loop = True
	while loop:
		visualizers.visualizeEverything()
		var.pyptr.display.flip()
		
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				loop = False

if __name__ == "__main__":
  main()