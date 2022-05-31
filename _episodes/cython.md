---
title: "Cython"
teaching: 15
exercises: 10
questions:
- "How slow is Python?"
- "Can I make my Python code faster?"
- "How can I turn my Python code into compiled C or C++ code?"
objectives:
- ""
keypoints:
- ""
---

Python is built for the programmer not the computer. What do I mean by that? Python is a very nice programming language to program in. You can get your ideas and algorithms written out very quickly as the Python language manages a lot of the aspects of memory management for you and provides convenient and flexible data structures that just work the way you expect them to without much effort on the part of the programmer to get it right. Part of this comes from the fact that Python is **"duck" typed**. Meaning, if a Python object looks like a duck, quacks like a duck, it is a duck. This means that you can pass different types of objects to a function and as long as that function can access the member functions of that object that it needs to work with it doesn't care what type of object you passed it. This allows you to **write code faster** and greatly increases the 
**flexibility** and **re-usability** of your Python code. However, **you pay for these benefits with your program run times**.

If you are are not doing any heavy computing this might be just fine, perhaps your CPUs wouldn't be doing that much work anyhow, and waiting another second to get your work done more than offsets the extra hours or days it might take you to write your algorithm out in another language like C of Fortran. However, if you are doing numerically intensive programming this can become a serious problem and is part of the reason why so much computationally intensive programs aren't written in Python.

One common solution to this problem is to take the parts of your Python program that are computational intensive and convert them to a compiled language that is much faster. One really nice thing about Python is how well integrated it is with C and C++. 

You can **extend** python with C or C++ by writing modules that you can import and use in your Python scripts in C. This however does take a bit of doing. Most of the extra effort involves creating the interfaces and Python objects to go between the C or C++ code and the Python scripts. For more details about how to do this see these [Python docs on extending Python with C or C++](https://docs.python.org/3/extending/extending.html).

You can also **embed** Python in a C or C++ application allowing it to call your Python functions from inside that application. This can be very handy for allowing scripting support within applications. For more details about embedding Python in C or C++ applications check these [Python docs on embedding Python in another application](https://docs.python.org/3/extending/embedding.html).

These two approaches are powerful, but do involve being very proficient at C and C++ and take a bit of doing to get working correctly. Though they provide the programmer with a lot of control in how the C or C++ portions of the application interface with the Python portions. If you are willing to give up some of this control for a short cut [**Cython**](https://cython.org/) is a good compromise.

Cython helps you compile your Python code into C code so that you can get the performance benefits of compiled language without having to do too much extra work to get there. Lets take a look at how we can use Cython.

In Python you can declare a variable as below.
~~~
x=0.5
~~~
{: .language-python}
You don't have to tell Python anything about the type of variable. In Python **everything is an object** (even floats and integers). This makes them super flexible but also more computationally and memory intensive.

One of the big differences in most compiled languages, and certainly is the case in both C and C++, is that **every variable must be declared** with a specific type. This means that at compile time the compiler has enough information about how something is going to work to perform more optimizations when generating the machine code that you will ultimately be running. In addition, if your floating point variable has a lot of extra baggage associated with it because it is actually a more complicated object, it can also increase memory requirements, which has impacts on performance as it might not fit as neatly into a cache line.

To allow Cython to generate compilable C and C++ code from our Python code we need to add some extra information about the types of our variables.

Some examples of how to do this with Cython is shown below.
~~~
cdef int a,b,c
cdef char *s
cdef float x=0.5
cdef double x=63.4
cdef list names
~~~
{: .language-python}

We also need to provide information about the return types and paramters of our functions and weather these functions will be called only from within the converted C code, `cdef`, or only from Python, `def`, or both, `cpdef`.
~~~
def test(x): #regular python function, calls from Python only
  ...
cdef int test(float x): #Cython only functions which can't be accessed from Python-only code.
  ...
cpdef int test2(float x, double y): #Can be accessed from either Cython or Python code.
  ...
~~~
{: .language-python}
Notice how the C/C++ variable types are showing up here as `int` the return type of the functions and the `float` or `double` types given for the function parameters.

Lets try this out in a full example.
~~~
$ cp hello.py dosum.py
$ nano dosum.py
~~~
{: .language-bash}

<div class="gitfile" markdown="1">
~~~
...
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
...
~~~
{: .language-python}
[dosum.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/dosum.py)
</div>

Lets quickly test it to make sure it works properly.
~~~
$ srun python dosum.py
~~~
{: .language-bash}
~~~
result=799999980000000.0 computed in 5.351787805557251s

----------------------------------------
wall clock time:5.352024793624878s
----------------------------------------
~~~
{: .output}

In preparation for speeding up our `sumnum` function with Cython lets pull it out into a separate Python module.
~~~
$ nano pysum.py
~~~
{: .language-bash}
<div class="gitfile" markdown="1">
~~~
def sumnum(n):
  result=0.0
  for i in range(n):
    result+=float(i)
  return result
~~~
{: .language-python}
[pysum.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/pysum.py)
</div>

Now copy and modify our original script to use our `sumnum` function from the newly created Python module and remove our old version of the `sumnum` function from the driver script.
~~~
$ cp dosum.py dosum_driver.py
$ nano dosum_driver.py
~~~
{: .language-bash}

~~~
import time
import pysum
...
def main():
  size=40000000
  start=time.time()
  result=pysum.sumnum(size)
  computeTime=elapsed(start)
  print("result="+str(result)+" computed in "+str(computeTime))
...
~~~
{: .language-python}

Verify everything still works.
~~~
$ srun python dosum.py
~~~
{: .language-bash}
~~~
result=799999980000000.0 computed in 5.351787805557251s

----------------------------------------
wall clock time:5.352024793624878s
----------------------------------------
~~~
{: .output}

Looks good. Now lets create a Cython version of our `pysum.py` module adding in the type declarations as mentioned previously.
~~~
$ cp pysum.py cysum.pyx
$ nano cysum.pyx
~~~
{: .language-bash}
<div class="gitfile" markdown="1">
~~~
cpdef float sumnum(int n):
  cdef float result=0.0
  cdef int i
  for i in range(n):
    result+=float(i)
  return result
~~~
{: .language-python}
[cysum.pyx](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/cysum.pyx)
</div>

Next create a `build_cysum.py` file which will act like a `Makefile` for compiling our `cysum.pyx` script.
~~~
$ nano build_cysum.py
~~~
{: .language-bash}
<div class="gitfile" markdown="1">
~~~
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('cysum.pyx'))
~~~
{: .language-python}
[build_cysum.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/build_cysum.py)
</div>

Then compile our Cython code with the following command.
~~~
$ python build_cysum.py build_ext --inplace
~~~
{: .language-bash}

Finally lets modify our driver script to use our newly created Cython version of the `sumnum` function and compare it to the old version.

~~~
$ nano dosum_driver.py
~~~
{: .language-bash}
<div class="gitfile" markdown="1">
~~~
import time
import pysum
import cysum
...
def main():
  size=40000000
  
  start=time.time()
  result=pysum.sumnum(size)
  computeTime=elapsed(start)
  print("pysum result="+str(result)+" computed in "+str(computeTime))
  
  start=time.time()
  result=cysum.sumnum(size)
  computeTime=elapsed(start)
  print("cysum result="+str(result)+" computed in "+str(computeTime))
...
~~~
{: .language-python}
[dosum_driver.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/dosum_driver.py)
</div>
~~~
$ srun nano dosum_driver.py
~~~
{: .language-bash}
~~~
pysum result=799999980000000.0 computed in 5.123960018157959s
cysum result=995504632627200.0 computed in 0.17841768264770508s

----------------------------------------
wall clock time:5.302709341049194s
----------------------------------------
~~~
{: .output}

Ok, so our Cython version is much faster, 5.12/0.17=30.12, so slightly more than 30 times faster. That's a pretty nice speed up for not a lot of work.

> ## Cythonize our compute-distributed.py script
> In the previous episode we had created a script that parallelized our `computePart` function across multiple distributed Dask workers. Lets now Cythonize that function to improve our performance even further to see if we can get below that approximately 3.4s of compute time when running with 4 workers having one core each.
>
> If you need a copy of that script you can download it with:
> ~~~
> $ wget https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed.py
> ~~~
> {: .language-bash}
> > ## Solution
> > Create a new module file containing our `computePart` function and "Cythonize" it.
> > ~~~
> > $ nano computePart.pyx
> > ~~~
> > {: .language-bash}
> > <div class="gitfile" markdown="1">
> > ~~~
> > cpdef int computePart(int size):
> >   cdef int part=0
> >   cdef int i
> >   for i in range(size):
> >     part=part+i
> >   return part
> > ~~~
> > {: .language-python}
> > [computePart.pyx](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/computePart.pyx)
> > </div>
> > Next create our file describing how we want to build our Cython module for the `computePart` function.
> > ~~~
> > $ nano build_computePart.py
> > ~~~
> > {: .language-bash}
> > <div class="gitfile" markdown="1">
> > ~~~
> > from distutils.core import setup
> > from Cython.Build import cythonize
> > 
> > setup(ext_modules=cythonize('computePart.pyx'))
> > ~~~
> > {: .language-python}
> > [build_computePart.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/build_computePart.py)
> > </div>
> > Then compile it.
> > ~~~
> > $ python build_computePart.py build_ext --inplace
> > ~~~
> > {: .language-bash}
> > Finally import our newly cythonized module and call the `computePart` function from it.
> > ~~~
> > $ cp compute-distributed.py compute-distributed-cython.py
> > $ nano compute-distributed-cython.py
> > ~~~
> > {: .language-bash}
> > <div class="gitfile" markdown="1">
> > ~~~
> > import time
> > import dask
> > from dask_jobqueue import SLURMCluster
> > from dask.distributed import Client
> > import computePart
> > ...
> > def main():
> > 
> >   size=40000000
> >   numParts=4
> >   numWorkers=4
> > 
> >   parts=[]
> >   for i in range(numParts):
> >     part=dask.delayed(computePart.computePart)(size)
> > ...
> > ~~~
> > {: .language-python}
> > [compute-distributed-cython.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed-cython.py)
> > </div>
> > Lets see the results.
> > ~~~
> > $ srun python compute-distributed-cython.py
> > ~~~
> > {: .language-bash}
> > ~~~
> > #!/usr/bin/env bash
> > 
> > #SBATCH -J dask-worker
> > #SBATCH -n 1
> > #SBATCH --cpus-per-task=1
> > #SBATCH --mem=245M
> > #SBATCH -t 00:05:00
> > 
> > /home/user49/dask/bin/python -m distributed.cli.dask_worker tcp://192.168.0.222:35157 --nthreads 1 --memory-limit 244.14MiB --name dummy-name --nanny --death-timeout 60 --protocol tcp://
> > 
> > 
> > =======================================
> > Compute time: 0.2513456344604492s
> > =======================================
> > 
> > 
> > ----------------------------------------
> > wall clock time:6.84865140914917s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > Now that compute time is down from about the 3.4s to 0.25s, that's a speed up of about 13 times faster. Remember the wall clock time is not super meaningful since we have added a 5s wait to help ensure the workers are all setup and ready before we do our computations.
> {: .solution}
{: .challenge}