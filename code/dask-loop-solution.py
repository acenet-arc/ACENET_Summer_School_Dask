from time import sleep
from dask import delayed

def inc(x):
  sleep(1)
  return x+1

def main():
  data=[1,2,3,4,5,6,7,8]
  results=[]
  for x in data:
    y=delayed(inc)(x)
    results.append(y)
  total=sum(results)
  total_num=total.compute()
  total.visualize()
  
  print("total is "+str(total_num))

if __name__=="__main__":
  main()
