import time
import dask
import numpy as np

def elapsed(start):
  return str(time.time()-start)+"s"

def computePart(size):
  return np.sum(np.ones(size))

def main():

  size=400000000
  numParts=4

  parts=[]
  for i in range(numParts):
    part=dask.delayed(computePart)(size)
    parts.append(part)
  sumParts=dask.delayed(sum)(parts)

  start=time.time()
  sumParts.compute()
  computeTime=elapsed(start)

  print()
  print("=======================================")
  print("Compute time: "+computeTime)
  print("=======================================")
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
