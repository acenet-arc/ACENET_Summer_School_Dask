import time

def elapsed(start):
  return str(time.time()-start)+"s"
def sumnum(n):
  result=0.0
  for i in range(n):
    result+=float(i)
  return result
def main():
  size=40000000
  start=time.time()
  result=sumnum(size)
  computeTime=elapsed(start)
  print("result="+str(result)+" computed in "+str(computeTime))
if __name__=="__main__":
  start=time.time()
  main()
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()
