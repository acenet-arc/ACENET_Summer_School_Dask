---
title: "Dask Array"
teaching: 15
exercises: 0
questions:
- ""
objectives:
- ""
keypoints:
- ""
start: true
---

Might be a nice way to visualize what is going on without doing something too complex to really be able to visualize
~~~
size=4
chunkFrac=0.5
x=dask.array.random.random((size,size),chunks=(int(size*chunkFrac),int(size*chunkFrac))
x.sum().visualize()
~~~
{: .python}


might be good to compare with just using numpy directly

#### NumPy version
~~~
import numpy as np
x=np.random.normal(10,0.1,size=(20000,20000))#400 million numbers, each 64 bits, total about 3.2GB
y=x.mean(axis=0)[::100]
~~~
{: .python}
needs GB of memory, and takes more than 10 seconds
#### Dask array vesrion
~~~
import numpy as np
import dask.array as da

x=da.random.nomral(10,0.1,size(20000,20000),chunks(1000,1000))# 400 million element array each 64 bits, cut into 1000x1000 sized chunks, 8MB/chunk, 20x20 chunks, can perform NumPy-style operations
y=x.mean(axis=0)[::100]
y.compute()
~~~
{: .python}
needs MB of memory and less time to execute

[Dask Array Docs][https://docs.dask.org/en/latest/array.html]
 - lists NumPy operations available
[best practices for Dask array](https://docs.dask.org/en/latest/array-best-practices.html)


-------------
* [Data Frames best practices](https://docs.dask.org/en/latest/dataframe-best-practices.html)
* [Delayed best practices](https://docs.dask.org/en/latest/delayed-best-practices.html)
* [General best practices](https://docs.dask.org/en/latest/best-practices.html)
* [Dask examples](https://examples.dask.org)



