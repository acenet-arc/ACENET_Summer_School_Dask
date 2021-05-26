---
title: "Dask - General"
teaching: 10
exercises: 5
questions:
- "What is Dask?"
objectives:
- "A thing we will do"
keypoints:
- "A key thing to know"
- "Another key thing to know"
---

## DASK - General

Dask is a lazy framework that automates parallel operations. Lazy, meaning that it doesn’t operate until it is told to.

Dask is conceptually similar to a dishwasher\*, where it will wait idle until it’s told to do everything all at once**.

*Using Dask does not guarantee your code will be clean.

**Not everything actually done all at once, Dask does several things at once.

## An artist's rendition of DASK before running based on my description
![](fig/Picture1.png)

## Dask - Distributed

Dask can operate as it’s own task manager in one of three ways:
1. Threaded – Using small, independent chunks of code running in the same instance of a computer program. Best for operations on numerical data that doesn’t keep a Global Interpreter Lock* (e.g. Numpy, Pandas, Scikit-Learn).
2. Processes – Sends data to separate instances of a program to be processed.  Generally works best when there are several instances of a program running at simultaneously that hold the Global Interpreter Lock*.
3. Single-Threaded – Does one chunk of code at a time, with no parallel capacity. Primarily for Debugging.

Parallel programming with Python has a complicated history because of a design decision, the Global Interpreter Lock, which limits python to a single thread most of the time. Global interperter lock is a complicated subject that I'm not prepared to digress into. If you really want to know about the GIL, [](https://realpython.com/python-gil/) , [https://en.wikipedia.org/wiki/Global_interpreter_lock](https://en.wikipedia.org/wiki/Global_interpreter_lock)

TL,DR:  Numpy, Pandas, and Scikit-Learn work around the problem using threads and Dask can work with that.

* Where I am running locally, I begin by spawning a client.  There are several different ways of doing this, however, we will be using a 4-core, 1 worker cluster, with a memory limit of 2GB of memory (adjust the memory req for whatever you can spare if you need to).
* This client will open up a "Dashboard" which you can use to monitor what's going on under the hood of your DASK instance.
* If you'd like to read more about specific clients, and how they operate, please refer to [https://distributed.dask.org/en/latest/](https://distributed.dask.org/en/latest/) as these features are difficult to use effectively on HPC systems
* We will not be delving deep into the distributed modules in Dask, as they are both very complex and do not work well with our HPC infrastructure, however, it is a powerful set of tools inside of the Dask kit, especially when operating on your local workstations.

**This is for me to create diagnostic reports, and your own if you review these notbooks 
You do not need to include this in any of your scripts**

~~~
from dask.distributed import Client, progress
client = Client(processes=False, threads_per_worker=4,
                n_workers=1, memory_limit='2GB')
client
~~~
{: .language-python}

## Dask - Delayed

* The Delayed command holds back the operations and assigns them to different cores.
* Rather than waiting for tasks to finish sequentially, initial tasks are assigned to different cores that operate simultaneously. 
* When a core finishes it’s job, it gets a new operation, similar to customs in an Airport.

We are going to demonstrate how dask.delayed works using an increment function that takes one second to execute, and and add function that takes one second to execute.

~~~
from time import sleep
from dask import delayed

def increment(x):
    sleep(1)
    return x + 1

def add(x, y):   
    sleep(1)
    return x +  y
~~~
{: .language-python}

This takes three seconds to run because we call each function sequentially, one after the other

~~~
x = increment(1)
y = increment(2)
z = add(x, y)
~~~
{: .language-python}

This runs immediately, all it does is build a graph

~~~
x = delayed(increment)(1)
y = delayed(increment)(2)
z = delayed(add)(x, y)
~~~
{: .language-python}

This actually runs our computation using a local process pool

~~~
z.compute()

z.visualize()
~~~
{: .language-python}

> ## Speeding up loops
>
> Use `Dask.Delayed` to improve the execution speed of this for loop
> ~~~
> output = []
> 
> for i in range(100):
>     j = increment(i)
>     output.append(j)
> 
> total = sum(output)
>     
> print(total)
> 
> ~~~
> {: .language-python}
> > ## answer 1
> > ~~~
> > output = []
> > for i in range(100):
> >     j = delayed(increment)(i)
> >     output.append(j)
> > 
> > total = sum(output)
> > 
> > total.compute()
> > 
> > total.visualize()
> > 
> > ~~~
> > {: .language-python}
> {: .solution}
> 
> > ## answer 2
> > ~~~
> > output = []
> > 
> > for i in range(100):
> >     j = delayed(increment)(i)
> >     output.append(j)
> >     
> > total = delayed(sum)(output)
> >     
> > total.compute()
> > 
> > total.visualize()
> > ~~~
> > {: .language-python}
> {: .solution}
> Note: When benchmarked with 1,000 and 10,000 samples of data on my hardware, the runtimes diverege as follows:
> 
> Serial:       1,000: 16:40       10,000: 2:47:40
> 
> Answer1:      1,000:  4:12       10,000: 0:42:27
> 
> Answer2:      1,000:  4:11       10,000: 0:42:25
{: .challenge}