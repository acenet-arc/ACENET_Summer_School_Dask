import time
import dask
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import computePartMod

def elapsed(start):
  return str(time.time()-start)+"s"

def main():

  size=40000000
  numParts=4
  numWorkers=4

  parts=[]
  for i in range(numParts):
    part=dask.delayed(computePartMod.computePart)(size)
    parts.append(part)
  sumParts=dask.delayed(sum)(parts)

  #create the "cluster"
  cluster=SLURMCluster(cores=1,memory="256M",walltime='00:05:00')

  #Show us the job script used to launch the workers
  print(cluster.job_script())
  client=Client(cluster)

  #create the workers
  cluster.scale(jobs=numWorkers)

  #sleep a little bit for workers to create and
  #check in with the scheduler
  time.sleep(5)

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
