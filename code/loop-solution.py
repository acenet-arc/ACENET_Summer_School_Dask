import time
import dask

def elapsed(start):
  return str(time.time()-start)+"s"

def inc(x):
  time.sleep(1)
  return x+1
def main():
  data=[1,2,3,4,5,6,7,8]
  dataInc=[]
  for x in data:
    y=dask.delayed(inc)(x)
    dataInc.append(y)
  total=dask.delayed(sum)(dataInc)
  total.visualize()
  result=total.compute()
  print("total="+str(result))

if __name__=="__main__":
  start=time.time()
  main()
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()