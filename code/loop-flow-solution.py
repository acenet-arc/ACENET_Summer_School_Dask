import time
import dask

def elapsed(start):
  return str(time.time()-start)+"s"

def inc(x):
  time.sleep(1)
  return x+1
def double(x):
  time.sleep(1)
  return 2*x
def isEven(x):
  return not x % 2
def main():
  data=[1,2,3,4,5,6,7,8,9,10]
  dataProc=[]
  for x in data:
    if isEven(x):
      y=dask.delayed(double)(x)
    else:
      y=dask.delayed(inc)(x)
    dataProc.append(y)

  total=dask.delayed(sum)(dataProc)
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
