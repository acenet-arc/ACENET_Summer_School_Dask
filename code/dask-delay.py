import time
import dask

def inc(x):
  time.sleep(1)
  return x+1
def add(x,y):
  time.sleep(1)
  return x+y

def main():
  x=dask.delayed(inc)(1)
  y=dask.delayed(inc)(2)
  z=dask.delayed(add)(x,y)
  z.visualize()
  result=z.compute()
  print("result="+str(result))
if __name__=="__main__":
  start=time.time()
  main()
  end=time.time()
  print("wall clock time:"+str(end-start)+"s")
