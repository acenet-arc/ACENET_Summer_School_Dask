from time import sleep
from dask import delayed

def inc(x):
  sleep(1)
  return x+1

def main():
  data=[1,2,3,4,5,6,7,8]
  results=[]
  for x in data:
    y=inc(x)
    results.append(y)
  total=sum(results)
  print("total is "+str(total))

if __name__=="__main__":
  main()
