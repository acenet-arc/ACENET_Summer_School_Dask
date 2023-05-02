import time

def elapsed(start):
  return str(time.time()-start)+"s"
def main():
  print("hello world")

if __name__=="__main__":
  start=time.time()
  main()
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()
