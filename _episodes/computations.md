---
title: "Real Computations"
teaching: 15
exercises: 10
questions:
- "What happens when I use Dask for \"real\" computations?"
- "How can I see CPU efficiency of a SLURM Job?"
objectives:
- ""
keypoints:
- ""
---

So far we have seen how to use Dask delayed to speed up or parallelize the `time.sleep()` function. Lets now try it with some "real" computations.

Lets start with our `hello.py` script and add some functions that do some computations and used Dask `delayed` to parallelize them.

~~~
$ cp hello.py compute.py
$ nano compute.py
~~~

Then edit to contain the following.
<div class="gitfile" markdown="1">
~~~
import time
import dask

def elapsed(start):
  return str(time.time()-start)+"s"

def computePart(size):
  part=0
  for i in range(size):
    part=part+i
  return part

def main():

  size=40000000
  numParts=4

  parts=[]
  for i in range(numParts):
    part=dask.delayed(computePart)(size)
    parts.append(part)
  sumParts=dask.delayed(sum)(parts)

  start=time.time()
  sumParts.compute()
  computeTime=elapsed(start)

  print()
  print("=======================================")
  print("Compute time: "+computeTime)
  print("=======================================")
  print()

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
[compute.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute.py)
</div>


Lets run it.

~~~
$ srun --cpus-per-task=1 python compute.py
~~~
{: .language-bash}
~~~

=======================================
Compute time: 11.632155656814575s
=======================================


----------------------------------------
wall clock time:11.632789134979248s
----------------------------------------

~~~
{: .output}

> ## More cores!
> Take the `compute.py` code and run it with different numbers of cores like we 
> did for the `delayed.py` code. What do you expect to happen? What actually happens?
>
> > ## Solution
> > #### 1 core
> > ~~~
> > $ srun --cpus-per-task=1 python compute.py
> > ~~~
> > {: .language-bash}
> > ~~~
> > =======================================
> > Compute time: 11.632155656814575s
> > =======================================
> > 
> > 
> > ----------------------------------------
> > wall clock time:11.632789134979248s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > 
> > #### 2 cores
> > ~~~
> > $ srun --cpus-per-task=2 python compute.py
> > ~~~
> > {: .language-bash}
> > ~~~
> > =======================================
> > Compute time: 11.144386768341064s
> > =======================================
> > 
> > 
> > ----------------------------------------
> > wall clock time:11.14497971534729s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > 
> > #### 4 cores
> > ~~~
> > $ srun --cpus-per-task=4 python compute.py
> > ~~~
> > {: .language-bash}
> > ~~~
> > =======================================
> > Compute time: 11.241060972213745s
> > =======================================
> > 
> > 
> > ----------------------------------------
> > wall clock time:11.241632223129272s
> > ----------------------------------------
> > ~~~
> > Shouldn't they be approximately dividing up the work, but the times are all about the same?
> > {: .output}
> {: .solution}
{: .challenge}

In the last exercise we learned that our "computations" do not parallelize as well as the `time.sleep()` function did previously. To explore this lets take a look at the CPU efficiency of our jobs. To do this we can use the `seff` command which outputs stats for a job after it has completed given the **JobID** including the CPU efficiency. But where do we get the JobID? To get the JobID we can run our jobs in the background by appending the `&` character to our `srun` command. Once we have our job running in the background we check on it in the queue to get the JobID.

To make it a little easier to see what is going on in our queue lets create an alias for the `squeue` command with some extra options.

~~~
$ alias sqcm="squeue -u $USER -o'%.7i %.9P %.8j %.6u %.2t %.5M %.5D %.4C %.5m %N'"
~~~
{: .language-bash}

Now we can run the command `sqcm` and get only our jobs (not everyones) and also additional information about our jobs, for example how many cores and how much memory was requested.

Lets run a job now and try it out.
~~~
$ srun --cpus-per-task=1 python compute.py&
$ sqcm
~~~
{: .language-bash}
~~~
 JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    964 cpubase_b   python user49  R  0:10     1    1  256M node-mdm1
$
=======================================
Compute time: 11.121154069900513s
=======================================


----------------------------------------
wall clock time:11.121747255325317s
----------------------------------------
~~~
{: .output}

I got the output from our `sqcm` command followed a little later by the output of our job. It is important to run the `sqcm` command before the job completes or you won't get to see the JobID.

Our `sqcm` command showed us that our job was running with one CPU on one node and with 256M of memory. It also shows us how long the job has run for and let us see the JobID.

When the `srun` command is running in the background I found I had to press the return key to get my prompt back and at the same time got a message about my background `srun` job completing.
~~~
[1]+  Done                    srun --cpus-per-task=1 python compute.py
$
~~~
{: .output}

With the JobID we can use the `seff` command to see what the cpu efficiency was.

~~~
$ seff 965
~~~
{: .language-bash}

~~~
Job ID: 965
Cluster: pcs
User/Group: user49/user49
State: COMPLETED (exit code 0)
Cores: 1
CPU Utilized: 00:00:11
CPU Efficiency: 84.62% of 00:00:13 core-walltime
Job Wall-clock time: 00:00:13
Memory Utilized: 0.00 MB (estimated maximum)
Memory Efficiency: 0.00% of 256.00 MB (256.00 MB/core)
~~~
{: .output}

We got almost 85% CPU efficiency, not too bad.

> ## CPU efficiency
> Given what we just learned about how to check on a jobs efficiency, lets
> re-run our dask jobs with different numbers of cores 1,2,4 and see what the
> CPU efficiency is.
> > ## Solution
> > #### 1 core
> > ~~~
> > $ srun --cpus-per-task=1 python compute.py&
> > $ sqcm
> > ~~~
> > {: .language-bash}
> > ~~~
> >   JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
> >     966 cpubase_b   python user49  R  0:04     1    1  256M node-mdm1
> > ~~~
> > {: .output}
> > ~~~
> > $ seff 966
> > ~~~
> > {: .language-bash}
> > ~~~
> > Job ID: 966
> > Cluster: pcs
> > User/Group: user49/user49
> > State: COMPLETED (exit code 0)
> > Cores: 1
> > CPU Utilized: 00:00:11
> > CPU Efficiency: 91.67% of 00:00:12 core-walltime
> > Job Wall-clock time: 00:00:12
> > Memory Utilized: 0.00 MB (estimated maximum)
> > Memory Efficiency: 0.00% of 256.00 MB (256.00 MB/core)
> > ~~~
> > {: .output}
> > #### 2 cores
> > ~~~
> > $ srun --cpus-per-task=2 python compute.py&
> > $ sqcm
> > ~~~
> > {: .language-bash}
> > ~~~
> >   JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
> >     967 cpubase_b   python user49  R  0:04     1    2  256M node-mdm1
> > ~~~
> > {: .output}
> > ~~~
> > $ seff 967
> > ~~~
> > {: .language-bash}
> > ~~~
> > Job ID: 967
> > Cluster: pcs
> > User/Group: user49/user49
> > State: COMPLETED (exit code 0)
> > Nodes: 1
> > Cores per node: 2
> > CPU Utilized: 00:00:12
> > CPU Efficiency: 50.00% of 00:00:24 core-walltime
> > Job Wall-clock time: 00:00:12
> > Memory Utilized: 12.00 KB
> > Memory Efficiency: 0.00% of 512.00 MB
> > ~~~
> > {: .output}
> > #### 4 cores
> > ~~~
> > $ srun --cpus-per-task=4 python compute.py&
> > $ sqcm
> > ~~~
> > {: .language-bash}
> > ~~~
> >   JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
> >     968 cpubase_b   python user49  R  0:04     1    4  256M node-mdm1
> > ~~~
> > {: .output}
> > ~~~
> > $ seff 968
> > ~~~
> > {: .language-bash}
> > ~~~
> > Job ID: 968
> > Cluster: pcs
> > User/Group: user49/user49
> > State: COMPLETED (exit code 0)
> > Nodes: 1
> > Cores per node: 4
> > CPU Utilized: 00:00:12
> > CPU Efficiency: 25.00% of 00:00:48 core-walltime
> > Job Wall-clock time: 00:00:12
> > Memory Utilized: 4.00 KB
> > Memory Efficiency: 0.00% of 1.00 GB
> > ~~~
> > {: .output}
> > The efficiencies are ~ 92%, 50%, and 25% for 1,2,4 CPUs respectively. It looks like very little if any of these threads are running in parallel.
> {: .solution}
{: .challenge}

What is going on, where did our parallelism go? Remember the Global Interpreter Lock (GIL) I mentioned way back at the beginning? Well that's what is going on! When a thread needs to use the Python interpreter it locks access to the interpreter so no other thread can access it, when it is done it releases the lock and another thread can use it. This means that no single thread can execute Python code at the same time!

But why did our `sleep` function work? When we used the `sleep` function, the waiting happens outside the Python interpreter. In this case each thread will happily wait in parallel since the 'work' inside the `sleep` function doesn't have to wait for the Python interpreter to become free and so they can run in parallel. This goes for any other function calls that do not run in the Python interpreter, for example NumPy operations often run as well-optimized C code and don't need the Python interpreter to operate, however it can be tricky to know exactly when and how the Python interpreter will be needed.

Does this mean Dask is not that great for parallelism? Well, the way we have used it so far can be useful in certain circumstances, for example what I mentioned about NumPy above, however there is another way you can use Dask, and that is in a distributed way. Lets look at that now!

<!--


[distributed, multiprocessing, processes, single-threaded, sync, synchronous, threading, threads]



- single thread
  - no parallelism
  - executes in computation sequentially in current thread
  - useful for debugging

- threads
  - default choice
  - works well for code that spends a lot of time NOT executing Python code due to GIL
  - e.g. i/o, compiled C code like Numpy, Pandas, Scikit-Learn, etc.

- Processes
  - works well for code that spends a lot of time executing Python code
  - each process has its own Python interpreter
  - takes longer to start up than threads

- distributed
  - useful for asynchronous and larger workloads
  - can be used on a single machine or scaled out to many machines
  - must deploy a dask cluster
  - launch multiple workers
  (launch dask-schedular, and dask-workers registered with schedular)
  - dask mpi? Do I want to talk about this? Need to provide a schedular_file.json file what is that?
  
  srun python dask-slurm-job-launcher.py
  
===========
Exercises
  
  alias sqcm="squeue -u $USER -o'%.7i %.9P %.8j %.6u %.2t %.5M %.5D %.4C %.5m %N'"
  
  srun --cpus-per-task=1 python dask-delay-python-dasked.py&
  sqcm
  
  Whats the compute time?
  ====================================
  Compute time: 11.320246458053589s
  ====================================
  
  seff
  
  What's the CPU efficiency
  
  ------
  
  srun --cpus-per-task=2 python dask-delay-python-dasked.py&
  sqcm
  
  Whats the compute time?
  
  seff
  
  What's the CPU efficiency
  
  ------
  
  srun --cpus-per-task=4 python dask-delay-python-dasked.py&
  sqcm
  
  What's the compute time?
  
  seff
  What's the CPU efficiency
  
  ------
  
  srun --cpus-per-task=8 python dask-delay-python-dasked.py&
  sqcm
  
  What's the compute time?
  
  seff
  What's the CPU efficiency
  
  All the compute times are about the same! And the CPU efficiency keeps going down What's up? Turns out this is because of GIL. The operations in that script all make use of the Python interpreter and so while they are running the tasks in multiple threads each thread has to take turns accessing the Python interpreter so in reality there is no parallelism at all happening here.
  
  
  How to fix it? Dask distributed!
  
  srun python dask-delay-python-dasked-distributed.py&
  
  size=40000000
  numParts=4
  numWorkers=1
  ====================================
  Compute time: 12.333828449249268s
  ====================================
  
  numWorkers=2
  ====================================
  Compute time= 6.07476544380188s
  ====================================
  
  numWorkers=4
  ====================================
  Compute time= 3.454866409301758s
  ====================================
  
  numWorkers=8
  ====================================
  Compute time= 3.3805696964263916s
  ====================================

-->