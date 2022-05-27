---
title: "Dask Schedulers"
teaching: 15
exercises: 20
questions:
- "What are the different ways I can run my tasks in parallel?"
objectives:
- ""
keypoints:
- ""
---

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