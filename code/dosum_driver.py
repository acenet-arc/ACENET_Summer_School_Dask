import time
import pysum
import cysum

def elapsed(start):
  return str(time.time()-start)+"s"
def main():
  size=40000000

  start=time.time()
  result=pysum.sumnum(size)
  computeTime=elapsed(start)
  print("pysum result="+str(result)+" computed in "+str(computeTime))

  start=time.time()
  result=cysum.sumnum(size)
  computeTime=elapsed(start)
  print("cysum result="+str(result)+" computed in "+str(computeTime))
if __name__=="__main__":
  start=time.time()
  main()
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()
