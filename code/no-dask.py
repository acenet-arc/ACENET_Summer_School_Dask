import time

def inc(x):
  time.sleep(1)
  return x+1
def add(x,y):
  time.sleep(1)
  return x+y

def main():
  x=inc(1)
  y=inc(2)
  z=add(x,y)
  print("z="+str(z))
if __name__=="__main__":
  start=time.time()
  main()
  end=time.time()
  print("wall clock time:"+str(end-start)+"s")
