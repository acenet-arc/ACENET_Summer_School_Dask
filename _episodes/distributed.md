---
title: "Distributed Computations"
teaching: 25
exercises: 15
questions:
- "How can I avoid the GIL problem?"
- "How can I run multiple Python interpreters at once on one problem?"
objectives:
- ""
keypoints:
- ""
#start: true
---

So we have started to see some of the implications of GIL when we are using Dask. Now we will look at a way to avoid it even if your code needs frequent access to the Python Interpreter (e.g. you haven't converted a bunch of it to C code with something like [Cython](https://cython.org/) which can seriously improve the performance of Python code even before parallelization).

The basic idea with distributed computations is to give each execution of your Python code it's own Python interpreter. This means that there will necessarily be massage passing and coordinating between the different processes running the different Python interpreters. Luckily Dask takes care of all this for us and after a bit of additional setup we can use it with `Delayed` just as we did before but without issues with GIL.

Since we are coming back from last day we have to log back into the cluster and re-activate our virtual environment.

~~~
$ ssh -X <your-username>@pcs.ace-net.training
$ source ~/dask/bin/activate
~~~
{: .language-bash}

Lets also re-do our `squeue` alias as we will want that. To make this permanent you could put this line into your `~/.bashrc` file.
~~~
$ alias sqcm="squeue -u $USER -o'%.7i %.9P %.8j %.7u %.2t %.5M %.5D %.4C %.5m %N'"
~~~
{: .language-bash}

Lets start with our previous `compute.py` script and modify it to run in a distributed way.

~~~
$ cp compute.py compute-distributed.py
$ nano compute-distributed.py
~~~
{: .language-bash}

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

  client.close()
  cluster.close()
...
~~~
{: .language-python}
[compute-distributed.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed.py)
</div>

In the above script we have added a few bits. We have imported `SLURMCluster` which allows us to submit jobs to create independent Dask workers and we have imported the Dask `Client` so that we can tell it to use the software Dask cluster we create.

We can create some number of workers using the `cluster.scale(numWorkers)` function. After these setup bits our computation continues as normal with Dask `Delayed`.

Lets run our new script, this time the computation is all done in the workers and not in the job we submit with the `srun` command. There is no need to change the number of CPUs we request as that is all taken care of by changing the `numWorkers` variable. Lets also immediately run the `sqcm` command to see what jobs we have running and frequently afterwards to see how Dask spawns new workers for us.
~~~
$ srun python compute-distributed.py&
$ sqcm
~~~
{: .language-bash}
~~~
  JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    980 cpubase_b   python user49  R  0:02     1    1  256M node-mdm1
~~~
{: .output}
Here you can just see our first job we submitted.
~~~
$ sqcm
~~~
{: .language-bash}
~~~
  JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    981 cpubase_b dask-wor user49 PD  0:00     1    1  245M
    980 cpubase_b   python user49  R  0:04     1    1  256M node-mdm1
~~~
{: .output}
Here you can see the worker job that Dask spawned for our work is in the `PD` or pending state.
~~~
$ sqcm
~~~
{: .language-bash}
~~~
  JOBID PARTITION     NAME   USER ST  TIME NODES CPUS MIN_M NODELIST
    980 cpubase_b   python user49  R  0:07     1    1  256M node-mdm1
    981 cpubase_b dask-wor user49  R  0:02     1    1  245M node-mdm1
~~~
{: .output}
Finally here we see that the worker is up and running.
~~~
#SBATCH -J dask-worker
#SBATCH -n 1
#SBATCH --cpus-per-task=1
#SBATCH --mem=245M
#SBATCH -t 00:05:00

/home/user49/dask/bin/python -m distributed.cli.dask_worker tcp://192.168.0.133:44075 --nthreads 1 --memory-limit 244.14MiB --name dummy-name --nanny --death-timeout 60
~~~
{: .output}
Above we see a print out of the job script that Dask uses to launch our workers. The settings for this script come from the settings we gave to the `SLURMCluster` function.

~~~
=======================================
Compute time: 12.071980953216553s
=======================================


----------------------------------------
wall clock time:18.724435329437256s
----------------------------------------
~~~
{: .output}
And finally we get our timings for performing our computations. A little longer than with our pur Dask Delayed code, but lets see how it changes with more cores, or rather more workers.

> ## More cores distributed
> Given the above `compute-distributed.py` run first with `numWorkers=1` to get a base line, then run with `numWorkers=2`, `4`, and `8`.
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
