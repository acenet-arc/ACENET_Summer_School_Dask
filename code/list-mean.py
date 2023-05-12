import time
import numpy as np

def elapsed(start):
  return str(time.time()-start)+"s"

def meanOfList(a):
  sum=0.0
  for item in a:
    sum+=item
  return sum/float(len(a))
def main():
  
  #about 380M of random numbers
  dim=50000000

  randomList=np.random.normal(0.0,0.1,size=dim).tolist()

  start=time.time()
  mean=meanOfList(randomList)
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
