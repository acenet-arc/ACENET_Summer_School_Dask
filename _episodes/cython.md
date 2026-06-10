---
title: "Cython"
teaching: 25
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

If you are are not doing any heavy computing this might be just fine, perhaps your CPUs wouldn't be doing that much work anyhow, and waiting another second to get your work done more than offsets the extra hours or days it might take you to write your algorithm out in another language like C or Fortran. However, if you are doing numerically intensive programming this can become a serious problem and is part of the reason most computationally intensive programs aren't written in Python.

One common solution to this problem is to take the parts of your Python program that are computational intensive and convert them to a compiled language that is much faster. One really nice thing about Python is how well integrated it is with C and C++. 

You can **extend** python with C or C++ by writing modules that you can import and use in your Python scripts. This however does take a bit of doing. Most of the extra effort involves creating the interfaces and Python objects to go between the C or C++ code and the Python scripts. For more details about how to do this see these [Python docs on extending Python with C or C++](https://docs.python.org/3/extending/extending.html).

You can also **embed** Python in a C or C++ application allowing it to call your Python functions from inside that application. This can be very handy for allowing scripting support within applications. For more details about embedding Python in C or C++ applications check these [Python docs on embedding Python in another application](https://docs.python.org/3/extending/embedding.html).

These two approaches are powerful, but do involve being very proficient at C and C++ and take a bit of doing to get working correctly. Though they provide the programmer with a lot of control in how the C or C++ portions of the application interface with the Python portions. If you are willing to give up some of this control for a short cut [**Cython**](https://cython.org/) is a good compromise.

Cython helps you compile your Python code into C code so that you can get the performance benefits of a compiled language without having to do too much extra work to get there. But before we get too far into Cython, lets install it so it is ready to go.

~~~
$ pip install cython
~~~
{: .language-bash}

Now that Cython is installed lets take a look at how we can use it.

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

We also need to provide information about the return types and parameters of our functions and weather these functions will be called only from within the converted C code, `cdef`, or only from Python, `def`, or both, `cpdef`.
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
$ srun python dosum_driver.py
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
cpdef double sumnum(int n):
  cdef double result=0.0
  cdef int i
  for i in range(n):
    result+=i
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

The `--inplace` tells python to build a shared object, `.so`, file in the current working directory rather than a library directory for compiled modules.

> ## Finding out more
> To see a list of available options and their descriptions, use the `--help`` option.
> ~~~
> $ python build_cysum.py --help build_ext
> ~~~
> {: .language-bash}
{: .callout}


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
$ srun python dosum_driver.py
~~~
{: .language-bash}
~~~
pysum result=799999980000000.0 computed in 5.7572033405303955s
cysum result=799999980000000.0 computed in 0.11868977546691895s

----------------------------------------
wall clock time:5.876289129257202s
----------------------------------------
~~~
{: .output}

Ok, so our Cython version is much faster, 5.75/0.12=47.91, so nearly  **48 times faster**. That's a pretty nice speed up for not a lot of work.

> ## Cythonize our compute-distributed.py script
> In the previous episode we had created a script that parallelized our `computePart` function across multiple distributed Dask workers. Lets now Cythonize that function to improve our performance even further to see if we can get below that approximately 3.4s of compute time when running with 4 workers having one core each.
>
> **Hint:** the C `int` data type, is only guaranteed to be 16 bits or larger. However, on most systems it is usually 32 bits. A signed 32 bit integer can represent the largest integer of 2^(32-1)-1=2,147,483,647. However, we know our result is 3,199,999,920,000,000. Which is significantly larger than that maximum. There is a C type `long long` which uses 64 bits to represent integers, which would be more than enough to represent our result (see [climits](https://cplusplus.com/reference/climits/)).
>
> If you need a copy of that script you can download it with:
> ~~~
> $ wget https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed.py
> ~~~
> {: .language-bash}
> > ## Solution
> > Create a new module file containing our `computePart` function and "Cythonize" it.
> > ~~~
> > $ nano computePartMod.pyx
> > ~~~
> > {: .language-bash}
> > <div class="gitfile" markdown="1">
> > ~~~
> > cpdef long long computePart(int size):
> >   cdef long long part=0
> >   cdef int i
> >   for i in range(size):
> >     part=part+i
> >   return part
> > ~~~
> > {: .language-python}
> > [computePartMod.pyx](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/computePartMod.pyx)
> > </div>
> > Next create our file describing how we want to build our Cython module for the `computePart` function.
> > ~~~
> > $ nano build_computePartMod.py
> > ~~~
> > {: .language-bash}
> > <div class="gitfile" markdown="1">
> > ~~~
> > from distutils.core import setup
> > from Cython.Build import cythonize
> > 
> > setup(ext_modules=cythonize('computePartMod.pyx'))
> > ~~~
> > {: .language-python}
> > [build_computePartMod.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/build_computePartMod.py)
> > </div>
> > Then compile it.
> > ~~~
> > $ python build_computePartMod.py build_ext --inplace
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
> > import dask_mpi as dm
> > import dask.distributed as dd
> > import computePartMod
> > ...
> > def main():
> >   dm.initialize(exit=True)
> >   client=dd.Client()
> > 
> >   size=40000000
> >   numParts=4
> > 
> >   parts=[]
> >   for i in range(numParts):
> >     part=dask.delayed(computePartMod.computePart)(size)
> >     parts.append(part)
> >   sumParts=dask.delayed(sum)(parts)
> > ...
> > ~~~
> > {: .language-python}
> > [compute-distributed-cython.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed-cython.py)
> > </div>
> > Lets see the results.
> > ~~~
> > $ srun --ntasks=3 python compute-distributed-cython.py
> > ~~~
> > {: .language-bash}
> > ~~~
> > ...
> > 2024-06-04 13:30:26,293 - distributed.core - INFO - Starting established connection to tcp://192.168.239.99:36209
> > 
> > =======================================
> > result=3199999920000000
> > Compute time: 0.05466485023498535s
> > =======================================
> > 
> > ----------------------------------------
> > wall clock time:1.8323471546173096s
> > ----------------------------------------
> > 
> > 2024-06-04 13:30:26,353 - distributed.scheduler - INFO - Receive client connection: Client-9a637db7-2276-11ef-8426-fa163efada25
> > ...
> > ~~~
> > {: .output}
> > Now that compute time is down from about the 9.4s with 1 worker down to 0.05s, that's a speed up of about 188 times. Lets now compare our 4 worker cases:
> > ~~~
> > $ srun --ntasks=6 python compute-distributed-cython.py
> > ~~~
> > {: .language-bash}
> > ~~~
> > ...
> > 2024-06-04 13:34:21,765 - distributed.core - INFO - Starting established connection to tcp://192.168.239.99:38105
> > 
> > =======================================
> > result=3199999920000000
> > Compute time: 0.03722333908081055s
> > =======================================
> > 
> > ----------------------------------------
> > wall clock time:1.827465534210205s
> > ----------------------------------------
> > 
> > 2024-06-04 13:34:21,809 - distributed.scheduler - INFO - Receive client connection: Client-26bb4be5-2277-11ef-8488-fa163efada25
...
> > ~~~
> > {: .output}
> > Now with 4 workers, we go from 2.37s to 0.037s or a speed up of 64 times. At this point, the computations are taking significantly less time than everything else (see the nearly identical wall clock times), so unless we did more computations, running in parallel doesn't really matter now that we have compiled our python code with Cython.
> {: .solution}
{: .challenge}
