import time

def main():
  print("hello world")

if __name__=="__main__":
  start=time.time()
  main()
  end=time.time()
  print("wall clock time:"+str(end-start)+"s")
