---
title: "Python"
teaching: 25
exercises: 0
questions:
- "What is a virtual environment?"
- "How can you time Python scripts?"
- "What is a simple way to run a Python script on a compute node?"
objectives:
- ""
keypoints:
- ""
---

Before we get to working with Dask we need to setup our Python environment, some basic timing of python code, and create a script that does something slightly interesting that we can use as a starting point to work with Dask.

## Virtual environment setup
Connect to the server using your own username and check to see if your x11 forwarding is working.
~~~
$ ssh -X <your-username>@pcs.ace-net.training
$ xclock
~~~
{: .language-bash}

You should now be connected to the training cluster and hopefully if you have an x11 server running you should see a little analog clock pop up in a window. If you can't get x11 forwarding working, it isn't the end of the world. There is one small exercise where you will have look at the solution to see the graph rather than viewing the image yourself.

Next load the Python module.
~~~
$ module load python
~~~
{: .language-bash}

There is a version of python already available on the login node, but for consistency between clusters it is better to use the python version available through module system. If we wanted we could specify a particular version of the Python module to load, with something like `module load python/3.8.10`. For more information about using modules see the [Alliance documentation on modules](https://docs.alliancecan.ca/wiki/Utiliser_des_modules/en).

Next lets create a python virtual environment for our dask work and activate it.
~~~
$ virtualenv --no-download dask
$ source ~/dask/bin/activate
~~~
{: .language-bash}

A Python virtual environment provides an isolated place to install different Python packages. You can create multiple virtual environments to install different packages or versions of packages and switch between them to keeping each environment separate from each other avoiding version conflicts. For more information about using virtual environments see the [Alliance documentation on python virtual environments](https://docs.alliancecan.ca/wiki/Python#Creating_and_using_a_virtual_environment).

## Running a Python script
Lets create a basic "hello world" python script and make sure we can run it as a starting point.
~~~
$ nano hello.py
~~~
{: .language-bash}

This starts the nano editor, editing a new file `hello.py`.

Lets create our first python script just to check that we have everything working. In the editor add the following code.

~~~
def main():
  print("hello world")

if __name__=="__main__":
  main()
~~~
{: .language-python}

Save and exit by pressing 'ctrl'+'x' answering 'y' when asked if you would like to save followed by pressing enter to accept the filename. 

This is a pretty standard way to create a Python script so that if you import it as a module the `main` function isn't executed but you can access all the functions defined in it. However if you run it on the command line the main function will be executed.

Lets run the script to see if everything is working.

~~~
$ python ./hello.py
~~~
{: .language-bash}

~~~
hello world
~~~
{: .output}

## Timing
Since we are going to be parellelizing code using Dask it is useful to see what effect our efforts have on the run time. Lets add some code to our `hello.py` script to time execution.
~~~
$ nano hello.py
~~~
{: .language-bash}
<div class="gitfile" markdown="1">
~~~
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

~~~
{: .language-python}
[hello.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/hello.py)
</div>
~~~
$ python hello.py
~~~
{: .language-bash}
~~~
hello world

----------------------------------------
wall clock time:2.574920654296875e-05s
----------------------------------------

~~~
{: .output}

# Running on a compute node
Next to run more computationally intensive scripts or to run with multiple cores it is best to run the job on a compute node. To run on a compute node the `srun` command can be used.

~~~
$ srun python hello.py
~~~
{: .language-bash}
~~~
hello world

----------------------------------------
wall clock time:7.867813110351562e-06s
----------------------------------------

~~~
{: .output}

This command runs our script on a compute node granting access to a single compute core. The `srun` command is perfect in this training environment but there other, likely better, ways to run the Alliance HPC clusters, for more info see the [Alliances documentation on running jobs](https://docs.alliancecan.ca/wiki/Running_jobs).

# A more interesting script
To let us see how Dask can be used to parallelize a python script lets first write a bit more interesting python script to parallelize with Dask in the next episode.

~~~
$ cp ./hello.py pre-dask.py
$ nano pre-dask.py
~~~
{: .language-bash}

<div class="gitfile" markdown="1">
~~~
import time

def elapsed(start):
  return str(time.time()-start)+"s"

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
  wallClock=elapsed(start)
  print()
  print("----------------------------------------")
  print("wall clock time:"+wallClock)
  print("----------------------------------------")
  print()
~~~
{: .language-python}
[pre-dask.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/pre-dask.py)
</div>

Save and exit and run on a compute node with the following command and take note of the runtime.
~~~
$ srun python ./pre-dask.py
~~~
{: .language-bash}
~~~
z=5

----------------------------------------
wall clock time:3.0034890174865723s
----------------------------------------

~~~
{: .output}
It takes about 3s which isn't too surprising since we have three function calls all with a 1s `sleep` in them. Clearly this sleep is dominating the run time. This is obviously artificial but will allows us to have a well understood compute requirements while we are exploring Dask.
