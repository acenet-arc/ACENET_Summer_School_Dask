---
title: "Dask Delay"
teaching: 15
exercises: 15
questions:
- ""
objectives:
- ""
keypoints:
- ""
---


## Virtual environment setup
Connect to the server and create a python virtual environment to work in.
~~~
$ ssh -X user49@pcs.ace-net.training
$ module load python
$ cd ~
$ virtualenv --no-download dask
$ source ~/dask/bin/activate
~~~
{: .bash}

There is a version of python already available on the login node, but for consistency between clusters it is better to use the python version available through module system.

## Running a Python script

~~~
$ nano hello.py
~~~
{: bash}

This starts the nano editor, editing a new file `hello.py`.

Lets create our first python script just to check that we have everything working. In the editor add the following code.

~~~
def main():
  print("hello world")

if __name__=="__main__":
  main()
~~~
{: .python}

Save and exit by pressing 'ctrl'+'x' answering 'y' when asked if you would like to save followed by pressing enter to accept the filename.

We can then run the script to see if everything is working.

~~~
$ python ./hello.py
~~~
{: .bash}

~~~
hello world
~~~
{: .output}

## Timing
Since we are going to be parellelizing code using Dask it is useful to see what effect our efforts have on the run time. Lets add some code to our `hello.py` script to time execution.
~~~
$ nano hello.py
~~~
{: .bash}
<div class="gitfile" markdown="1">
~~~
import time

def main():
  print("hello world")

if __name__=="__main__":
  start=time.time()
  main()
  end=time.time()
  print("wall clock time:"+str(end-start)+"s")
~~~
{: .python}
[hello.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/hello.py)
</div>
~~~
$ python hello.py
~~~
{: .bash}
~~~
hello world
wall clock time:5.316734313964844e-05s
~~~
{: .output}

# Running on a compute node
To run on a compute node the `srun` command can be used.

~~~
$ srun python hello.py
~~~
{: .bash}
~~~
hello world
wall clock time:7.867813110351562e-06s
~~~
{: .output}

This command runs our script on a compute node granting access to a single compute core.

# A more interesting script
To let us see how Dask can be used to parallelize a python script lets first write a bit more interesting python script to parallelize.

~~~
$ cp ./hello.py no-dask.py
$ nano no-dask.py
~~~
{: .bash}

~~~
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
~~~
{: .python}

Save and exit and run on a compute node with the following command.
~~~
$ srun python ./no-dask.py
~~~
{: .bash}
~~~
z=5
wall clock time:3.003295421600342s
~~~
{: .output}
It takes about 3s which isn't too surprising since we have three function calls all with a 1s `sleep` in them. Clearly this sleep is dominating the run time. This is obviously artificial but will allows us to have a well understood compute requirements while we are exploring Dask.

## Dask Delayed

Before we can use dask we must install it with the following command on the terminal.
~~~
$ pip install pandas numpy dask distributed graphviz bokeh dask_jobqueue mimesis requests matplotlib
~~~
{: .bash}

This actually installs lots of stuff, not just Dask, but should take around 2 minutes or a bit less. This will install dask into the virtual environment we setup and are currently working in.

Looking back at the Python code we have, the two calls to the `inc` functions *could* be called in parallel, because they are totally independent of one-another.

We can use `dask.delayed` on our functions to make them **lazy**. When we say **lazy** it means that those functions won't be called immediately. What happens instead is that it records what we want to compute as a task into a graph that we will run later using the `compute` member function on the object returned by the `dask.delayed` function. 

Lets add the new Dask code now.

~~~
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
  #result=z.compute()
  #print("result="+str(result))
if __name__=="__main__":
  start=time.time()
  main()
  end=time.time()
  print("wall clock time:"+str(end-start)+"s")
~~~
{: .python}

However, to illustrate that nothing happens until `z.compute()` is called lets comment it and the following print line out and run it.

~~~
$ srun python ./dask-delay.py
~~~
{: .bash}
~~~
wall clock time:0.00028586387634277344s
~~~
{: .output}

It clearly didn't call our `inc` or `add` functions as any one of those calls should take at least 1 s and the total time is well below 1s. Now lets uncomment the code and rerun it.

~~~
...

def main():
  ...
  result=z.compute()
  print("result="+str(result))
...
~~~
{: .python}

~~~
$ srun python ./dask-delay.py
~~~
{: .bash}
~~~
result=5
wall clock time:3.0056424140930176s
~~~
{: .output}

Hey, that's no faster than the non-dask version. In fact it is a very tiny bit slower. What gives? Well, we only ran it on one core. Lets try on two cores and see what hapens.

~~~
$ srun --cpus-per-task=2 python ./dask-delay.py
~~~
{: .bash}
~~~
result=5
wall clock time:2.004542350769043s
~~~
{: .output}

So it is clearly improving our runtime. To help us understand what Dask is doing we can use the `visualize` `delayed` object member function which creates a visualization of the graph Dask uses for our tasks.

~~~
...
def main():
  ...
  z.visualize()
  #result=z.compute()
  #print("result="+str(result))
...
~~~
{: .python}

~~~
$ python ./dask-delay.py
~~~
{: .bash}

Which returns fairly quickly because we aren't actually doing any work. However it has created a `mydask.png` file which lets us visualize what Dask will do. Lets have a look at it (this requires the -X option to work and a x11 server running).

~~~
$ feh mydask.png
~~~
{: .bash}

![dask-delay.png](../fig/dask-delay.png)

Notice that this includes the names of the functions from our script and the logical flow of the outputs from the `inc` function to the inputs of the `add` function.

Here you can see that the two `inc` functions can be run in parallel provided we have hardware capable of running them at the same time and afterwards the `add` function will be run in serial.

> ## Challenge
> Apply what you have learned to parallelize the below loop with `dask.delayed`
> ~~~
> 
> ~~~
> {: .python}
> you can download with 
> ~~~
> $ wget https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/dask-loop-template.py
> ~~~
> > ## Solution
> > Solution text
> {: .solution}
{: .challenge}