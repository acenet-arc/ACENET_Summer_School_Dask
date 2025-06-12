import time
import dask
import dask_mpi as dm
import dask.distributed as dd

def elapsed(start):
  return str(time.time()-start)+"s"

def computePart(size):
  part=0
  for i in range(size):
    part=part+i
  return part

def main():
  dm.initialize(local_directory="/tmp")
  client=dd.Client()

  size=40000000
  numParts=4

  parts=[]
  for i in range(numParts):
    part=dask.delayed(computePart)(size)
    parts.append(part)
  sumParts=dask.delayed(sum)(parts)

  start=time.time()
  result=sumParts.compute()
  computeTime=elapsed(start)

  print()
  print("=======================================")
  print("result="+str(result))
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
