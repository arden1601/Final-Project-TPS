import configs.variables as var
import time

def loop_time():
  current_time = time.time()
  if current_time - var.last_updated >= var.delay:
    var.last_updated = current_time
    adjust_time(1)

def adjust_time(min_dupe):
    addMin = 60 // var.clock_min_limit * min_dupe
    var.clock_min += addMin
    
    if var.clock_min >= 60 or var.clock_min < 0:
      var.clock_min = 0
      var.clock += 1 * min_dupe
    
    if var.clock >= var.clock_limit:
      var.clock = 0
    
    return 