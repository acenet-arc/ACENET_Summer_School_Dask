import time
import numpy as np

def elapsed(start):
  return str(time.time()-start)+"s"
def main():
  
  #about 380M of random numbers
  dim=50000000
  
  randomArray=np.random.normal(0.0,0.1,size=dim)
  
  start=time.time()
  mean=np.mean(randomArray)
  computeTime=elapsed(start)
  
  print("mean is "+str(mean))
  print()
  print("==================================")
  print("compute time: "+computeTime)
  print("==================================")
  print()
if __name__=="__main__":
  start=time.time()
  main()
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()
