---
title: "Dask - Delayed"
teaching: 15
exercises: 5-10
questions:
- ""
objectives:
- ""

keypoints: 
- "Dask is 'Lazy' and won't go until you tell it to go explicitly"
- "Another key thing to know"
---



<!--
**This is for me to create diagnostic reports, and your own if you review these notbooks 
You do not need to include this in any of your scripts**

~~~
from dask.distributed import Client, progress
client = Client(processes=False, threads_per_worker=4,
                n_workers=1, memory_limit='2GB')
client
~~~
{: .language-python}

-->

## Dask - Delayed

* The Delayed command holds back the operations and assigns them to different cores.
* Rather than waiting for tasks to finish sequentially, initial tasks are assigned to different cores that operate simultaneously. 
* When a core finishes it’s job, it gets a new operation, similar to customs in an Airport.

We are going to demonstrate how dask.delayed works using an increment function that takes one second to execute, and and add function that takes one second to execute.

~~~
$ nano no_delay.py
~~~
{: .bash}

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
