---
title: "Distributed Computations"
teaching: 15
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

The basic idea with distributed computations is to give each execution of your Python code it's own Python interpreter. This means that there will necessarily be message passing and coordinating between the different processes running the different Python interpreters. Luckily Dask takes care of all this for us and after a bit of additional setup we can use it with `Delayed` just as we did before but without issues with GIL.

Since we are coming back from last day we have to log back into the cluster and re-activate our virtual environment.

~~~
$ ssh -X <your-username>@pcs.ace-net.training
$ module load python mpi4py
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
import dask_mpi as dm
import dask.distributed as dd
...
def main():
  dm.initialize(local_directory="/tmp")
  client=dd.Client()
...
~~~
{: .language-python}
[compute-distributed.py](https://raw.githubusercontent.com/acenet-arc/ACENET_Summer_School_Dask/gh-pages/code/compute-distributed.py)
</div>

In the above script we imported the `dask_mpi` and `dask.distributed` modules. We then call the `initialize()` function from the `dask_mpi` module and create a client from the `dask.distibuted` module. In the `initialize()` function we also set where we want the workers to store temporary files with `local_directory="/tmp"`. The rest of the script stays as it was, that's it. We can now run our previous code in a distributed way in an MPI environment.

To run in an MPI Job, we have to specify the number of tasks `--ntasks` instead of `--cpus-per-task` as we have been doing (see [Running MPI Jobs](https://docs.alliancecan.ca/wiki/Running_jobs#MPI_job)).

The `initialize()` function we called, actually sets up a number of process for us. It creates a Dask Schedular on MPI rank 0, runs the client script on MPI rank 1, and workers on MPI ranks 2 and above. This means, to have at least one worker, we need to have at least 3 tasks. Or to put it another way, with 3 tasks we will have one worker task running all of our `computePart` function calls.

~~~
$ srun --ntasks=3 python compute-distributed.py
~~~
{: .language-bash}
~~~
...
2024-06-03 19:22:29,474 - distributed.core - INFO - Starting established connection to tcp://192.168.239.99:39851

=======================================
result=3199999920000000
Compute time: 9.414103507995605s
=======================================


----------------------------------------
wall clock time:11.231945753097534s
----------------------------------------

2024-06-03 19:22:38,896 - distributed.scheduler - INFO - Receive client connection: Client-a3f38f41-21de-11ef-8d0c-fa163efada25
2024-06-03 19:22:38,896 - distributed.core - INFO - Starting established connection to tcp://192.168.239.99:48638
...
~~~
{: .output}

Still getting the same result and about the same compute time as our previous Dask Delayed code, but lets see how it changes as we increase `--ntasks`.

> ## More cores distributed
> Given the above `compute-distributed.py` run first with `--ntasks=3` to get a base line, then run with `--ntasks=4`, `6`, and `10`.
> 
> > ## Solution
> > #### `--ntasks=3`: 1 worker
> > ~~~
> > =======================================
> > result=3199999920000000
> > Compute time: 9.448347091674805s
> > =======================================
> > ----------------------------------------
> > wall clock time:11.187263250350952s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > 
> > #### `--ntasks=4`: 2 workers
> > ~~~
> > =======================================
> > result=3199999920000000
> > Compute time: 4.76196813583374s
> > =======================================
> > ----------------------------------------
> > wall clock time:6.3794050216674805s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > 
> > #### `--ntasks=6`: 4 workers
> > ~~~
> > =======================================
> > result=3199999920000000
> > Compute time: 2.3769724369049072s
> > =======================================
> > ----------------------------------------
> > wall clock time:4.282535791397095s
> > ----------------------------------------
> > ~~~
> > {: .output}
> > 
> > #### `--ntasks=10`: 8 workers
> > ~~~
> > =======================================
> > result=3199999920000000
> > Compute time: 2.432898759841919s
> > =======================================
> > ----------------------------------------
> > wall clock time:4.277429103851318s
> > ----------------------------------------
> > ~~~
> > {: .output}
> Now we are getting some true parallelism. Notice how more than 4 workers doesn't improve things, why is that?
> {: .solution}
{: .challenge}
