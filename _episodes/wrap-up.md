---
title: "Wrapping Up"
teaching: 5
exercises: 
questions:
- "What did we learn?"
- "What next?"
objectives:
- ""
keypoints:
- ""
---

## Summary

* Dask uses `dask.delayed` to compute task graphs.
* These task graphs can then be later used to `compute` the result in either a multi-threaded or distributed way.
* Multi-threaded python only benefits from the parallelism if it does considerable work outside the Python interpreter because of the GIL (e.g. NumPy etc.).
* Distributed parallel Python code works well for most Python code but has a bit of an extra overhead for message-passing, start up/tear down of Dask cluster.
* Python code is slow, but Cython can be used to easily compile computationally intensive parts into faster C code.
* Dask Array provides a way to parallelize NumPy arrays either in a multi-threaded way for faster computing, or in a distributed way to reduce the individual compute node memory requirements and still give a reasonable speed up over serial execution.

## Futher reading
On topics we have covered there can be more to learn. Check out these docs.
* [Dask docs](https://docs.dask.org/en/stable/)
* [General best practices](https://docs.dask.org/en/latest/best-practices.html)
* [Dask examples](https://examples.dask.org)
* [Dask Delayed Docs](https://docs.dask.org/en/stable/delayed.html)
* [Delayed best practices](https://docs.dask.org/en/latest/delayed-best-practices.html)
* [Dask Array Docs](https://docs.dask.org/en/latest/array.html)
* [Best practices for Dask array](https://docs.dask.org/en/latest/array-best-practices.html)


There are also some main features of Dask we didn't talk about.

* [Dask DataFrames](https://docs.dask.org/en/stable/dataframe.html) which provide a [Pandas](https://pandas.pydata.org/) like interface. See also [Data Frames best practices](https://docs.dask.org/en/latest/dataframe-best-practices.html).
* [Dask Bag](https://docs.dask.org/en/stable/bag.html) which implements operations like, map,filter, fold, and groupby on collections of generic Python objects similar to [PyToolz](https://toolz.readthedocs.io/en/latest/) or a Pythonic version of [PySpark](https://spark.apache.org/docs/latest/api/python/).
* [Dask Futures](https://docs.dask.org/en/stable/futures.html) which supports a real-time task framework, similar to `dask.delayed` but is immediate rather than lazy.