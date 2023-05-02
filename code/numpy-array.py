import time
import numpy as np

def elapsed(start):
  return str(time.time()-start)+"s"
def main():
  a=np.array([1,2,3,4,5])
  b=np.random.normal(0.0,0.1,size=5)
  print("a="+str(a))
  print("b="+str(b))

if __name__=="__main__":
  start=time.time()
  main()
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()
