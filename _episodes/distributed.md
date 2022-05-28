---
title: "Distributed Computations"
teaching: 10
exercises: 10
questions:
- "How can I avoid the GIL problem?"
objectives:
- ""
keypoints:
- ""
---

So we have started to see some of the implications of GIL when we are using Dask. Now we will look at a way to avoid it even if your code needs frequent access to the Python Interpreter (e.g. you haven't converted a bunch of it to C code with something like [Cython](https://cython.org/) I would recommend checking this out by the way as it will make even your parallel Python code run faster).

The basic idea here is to give each run your Python code in a distributed way so that each execution of your code has it's own Python interpreter. This means that there will necessarily be massage passing and coordinating between the different processes running the different Python interpreters. Luckily Dask takes care of all this for us and after a bit of additional setup we can use it with `Delayed` just as we did before but without issues with GIL.

Lets start with our previous `compute.py` script and modify it to run in a distributed way.

~~~
$ cp compute.py compute-distributed.py
$ nano compute-distributed.py
~~~
{: .bash}
<div class="gitfile" markdown="1">
~~~
import time
import dask
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
...
def main():

  size=40000000
  numParts=4
  numWorkers=1

  parts=[]
  for i in range(numParts):
    part=dask.delayed(computePart)(size)
    parts.append(part)
  sumParts=dask.delayed(sum)(parts)

  #create the "cluster"
  cluster=SLURMCluster(cores=1,memory="256M",walltime='00:05:00')

  #Show us the job script used to launch the workers
  print(cluster.job_script())
  client=Client(cluster)

  #create the workers
  cluster.scale(numWorkers)

  #sleep a little bit for workers to create and
  #check in with the scheduler
  time.sleep(5)

  start=time.time()
  sumParts.compute()
  computeTime=elapsed(start)
...
~~~
{: .python}
[compute-distributed.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed.py)
</div>

~~~
$ srun python compute-distributed.py&
$ sqcm
~~~
{: .bash}
~~~
  JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    980 cpubase_b   python user49  R  0:02     1    1  256M node-mdm1
~~~
{: .output}
~~~
$ sqcm
~~~
{: .bash}
~~~
  JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    981 cpubase_b dask-wor user49 PD  0:00     1    1  245M
    980 cpubase_b   python user49  R  0:04     1    1  256M node-mdm1
~~~
{: .output}
~~~
$ sqcm
~~~
{: .bash}
~~~
  JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    980 cpubase_b   python user49  R  0:07     1    1  256M node-mdm1
    981 cpubase_b dask-wor user49  R  0:02     1    1  245M node-mdm1
~~~
{: .output}
~~~
#SBATCH -J dask-worker
#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --mem=245M
#SBATCH -t 00:05:00

/home/user49/dask/bin/python -m distributed.cli.dask_worker tcp://192.168.0.133:44075 --nthreads 1 --memory-limit 244.14MiB --name dummy-name --nanny --death-timeout 60 --protocol tcp://
~~~
{: .output}
~~~
=======================================
Compute time: 12.071980953216553s
=======================================


----------------------------------------
wall clock time:18.724435329437256s
----------------------------------------
~~~
{: .output}

> ## More cores distributed
> Given the above `compute-distributed.py` run first with `numWorkers=1` to get a base line then run with `numWorkers=2`, `4`, and `8`.
> 
> **HINT:** you don't need to change the `srun python compute-distributed.py&` command as you change the number of workers.
> > ## Solution
> > #### numWorkers=1
> > ~~~
> > ====================================
> > Compute time: 12.333828449249268s
> > ====================================
> > ~~~
> > {: .output}
> > 
> > #### numWorkers=2
> > ~~~
> > ====================================
> > Compute time= 6.07476544380188s
> > ====================================
> > ~~~
> > {: .output}
> > 
> > #### numWorkers=4
> > ~~~
> > ====================================
> > Compute time= 3.454866409301758s
> > ====================================
> > ~~~
> > {: .output}
> > 
> > #### numWorkers=8
> > ~~~
> > ====================================
> > Compute time= 3.3805696964263916s
> > ====================================
> > ~~~
> > {: .output}
> Now we are getting some true parallelism. Notice how more than 4 workers doesn't improve things, why is that?
> {: .solution}
{: .challenge}

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