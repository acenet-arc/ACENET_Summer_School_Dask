import time
import numpy as np

def elapsed(start):
  return str(time.time()-start)+"s"
def main():

  #about 6G of random numbers
  dim=50000000*16

  start=time.time()
  randomArray=np.random.normal(0.0,0.1,size=dim)
  mean=randomArray.mean()
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
