from time import sleep

def inc(x):
  sleep(1)
  return x+1
def add(x,y):
  sleep(1)
  return x+y

def main():
  for i in range(10):
    x=inc(1)
    y=inc(2)
    z=add(x,y)

  print("z is "+str(z))

if __name__=="__main__":
  main()

