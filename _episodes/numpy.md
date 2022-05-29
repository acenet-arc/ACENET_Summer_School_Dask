---
title: "NumPy"
teaching: 10
exercises: 5
questions:
- "Why are NumPy arrays faster than lists?"
- "How do you create NumPy arrays?"
- "What are some things I can do with NumPy arrays?"
objectives:
- ""
keypoints:
- ""
start: true
---

At the beginning of this workshop I mentioned that Dask tries to provide familiar interfaces to well known Python libraries. One of these libraries in NumPy lets take a quick look at NumPy now before we turn to the Dask array interface in the next episode, which quite closely mimics the NumPy interface.

NumPy, or Numerical Python, is a Python library used for working with arrays and performing operations on them. Python's main data structure for managing groups of things, including numbers, is the list. Lists are very flexible and support lots of operations such as appending and removing. However they are computationally very slow. NumPy aims to provide an array object that is up to 50x faster than traditional Python lists. NumPy arrays are faster than lists because they are stored at one continuous place in memory so processing large sections of NumPy arrays at once means that much more of the data to be processed is likely to already loaded into caches that the CPUs can operate on quickly.

NumPy is a Python library written partially in Python, but most of the parts that require fast computations are written in C or C++. NumPy is a free and open source library and the source can be viewed on [github](https://github.com/numpy/numpy) if you like.

To use NumPy you need to install it. Luckily we already have it. If you remember back to the long list of libraries we installed using the `pip` command when installed Dask, `numpy` was included in that list. However, since we are coming back from last day we have to log back into the cluster and re-activate our virtual environment.

~~~
$ ssh -X <your-username>@pcs.ace-net.training
$ source ~/dask/bin/activate
~~~
{: .language-bash}

Lets also re-do our `squeue` alias as we will want that. To make this permenant you could put this line into your `~/.bashrc` file.
~~~
$ alias sqcm="squeue -u $USER -o'%.7i %.9P %.8j %.6u %.2t %.5M %.5D %.4C %.5m %N'"
~~~
{: .language-bash}

To use numpy in a Python script you would import it as any other module. Then you can create numpy arrays from regular python lists or using other specialized functions for example the [`normal`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html) function which creates an array of values in a normal distribution. The arguments to this function are the centre of the distribution (`0.0` in the code below), the standard deviation, (`0.1` below) and finally the `size` specifies the number of points to generate within that distribution.

~~~
$ cp hello.py numpy-array.py
$ nano numpy-array.py
~~~
{: .language-bash}

<div class="gitfile" markdown="1">
~~~
import time
import numpy as np
...
def main():
  a=np.array([1,2,3,4,5])
  b=np.random.normal(0.0,0.1,size=5)
  print("a="+str(a))
  print("b="+str(b))
...
~~~
{: .language-python}
[numpy-array.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/numpy-array.py)
</div>

~~~
$ python numpy-array.py
~~~
{: .language-bash}
~~~
a=[1 2 3 4 5]
b=[ 0.05223141  0.06349035 -0.13371892  0.10936532 -0.04647926]

----------------------------------------
wall clock time:0.0010428428649902344s
----------------------------------------
~~~
{: .output}

You can slice NumPy arrays like this `[start:end:step]` for example
~~~
a[1:4:2]
~~~
{: .language-python}
would be the array
~~~
[2 4]
~~~
{: .output}

You can also do operations between NumPy arrays for example the element wise multiplication of two NumPy arrays.
~~~
a*b
~~~
{: .language-python}
~~~
[-0.00971874 -0.32869994  0.20848835 -0.14110609  0.6818243 ]
~~~
{: .output}

There are lots of [arithmetic, matrix multiplication, and comparison operations](https://numpy.org/doc/stable/reference/arrays.ndarray.html#arithmetic-matrix-multiplication-and-comparison-operations) supported on NumPy arrays.

There are also more general [calculation](https://numpy.org/doc/stable/reference/arrays.ndarray.html#calculation) methods that can operate on the array as a whole or along a particular axis (or coordinate) of the array if the array is multi-dimensional. One example of such an NumPy array method is the [`mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html). Lets create our script that calculates the mean of a large NumPy array and time how long it takes.

~~~
$ cp numpy-array.py numpy-mean.py
$ nano numpy-mean.py
~~~
{: .language-bash}

<div class="gitfile" markdown="1">
~~~
import time
import numpy as np
...
def main():
  
  #about 380M of random numbers
  dim=50000000
  
  randomArray=np.random.normal(10.0,0.1,size=dim)
  
  start=time.time()
  mean=np.mean(randomArray)
  computeTime=elapsed(start)
  
  print("mean is "+str(mean))
  print()
  print("==================================")
  print("compute time: "+computeTime)
  print("==================================")
  print()
...
~~~
{: .language-python}
[numpy-mean.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/numpy-mean.py)
</div>

Lets run it, however, we need to specify an amount of memory when running this as it uses more than the default of 256M since it has about 380M of data alone.

~~~
$ srun --mem=1G python numpy-mean.py&
~~~
{: .language-bash}
~~~
mean is 8.622950594790064e-06

==================================
compute time: 0.04160046577453613s
==================================


----------------------------------------
wall clock time:2.0075762271881104s
----------------------------------------
~~~
{: .output}

> ## NumPy array vs. Python lists
> We just saw that we can calculate the mean of a NumPy array of more than 50 million points in well under a second. Lets run both the NumPy version and a Python list version and compare the times.
>
> You can download the list version with the following command.
> ~~~
> $ wget https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/list-mean.py
> ~~~
> {: .language-bash}
>
> **HINT**: the list version takes more memory than the numpy version to run, you might want to try using `--mem=3G` option on your `srun` command if you get errors like:
> ~~~
> slurmstepd: error: Detected 1 oom-kill event(s) in StepId=1073.0. Some of your processes may have been killed by the cgroup out-of-memory handler.
> srun: error: node-mdm1: task 0: Out Of Memory
> ~~~
> {: .output}
> > ## Solution
> > ~~~
> > $ srun --mem=3G python list-mean.py
> > ~~~
> > {: .output}
> > ~~~
> > mean is 4.242821579804046e-06
> > 
> > ==================================
> > compute time: 1.880323886871338s
> > ==================================
> > 
> > 
> > ----------------------------------------
> > wall clock time:6.4972100257873535s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > The NumPy version of the mean computation is `1.88/0.0416=46.2` times faster than the list version. Note that in the `list-mean.py` we cheat when creating the list by using the same `np.random.normal` function but then use the `tolist()` member function to convert the NumPy array to a list. Created the list element by element the overall `wall clock time` would be even larger.
> {: .solution}
{: .challenge}

NumPy arrays are clearly faster than lists, now lets see how we can use Dask to manage even larger NumPy like arrays and process them faster in parallel.





