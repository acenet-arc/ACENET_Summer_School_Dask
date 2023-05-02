import time
import dask.array as da
from dask_jobqueue import SLURMCluster
from dask.distributed import Client

def elapsed(start):
  return str(time.time()-start)+"s"
def main():

  #about 6G of random numbers
  dim=50000000*16
  numChunks=16
  numWorkers=4

  randomArray=da.random.normal(0.0,0.1,size=dim,chunks=(int(dim/numChunks)))
  meanDelayed=randomArray.mean()
  meanDelayed.visualize()

  #memory=6G data / 16chunks x 4 cores per worker =1.5G plus a little extra
  cluster=SLURMCluster(cores=1,memory="2G",walltime='00:05:00')
  client=Client(cluster)
  cluster.scale(numWorkers)
  time.sleep(5)

  start=time.time()
  mean=meanDelayed.compute()
  computeTime=elapsed(start)

  client.close()
  cluster.close()

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
