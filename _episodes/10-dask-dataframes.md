---
title: "Dask - Dataframes"
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

**When to use DataFrames (from the Dask documentation)**
> Dask DataFrames are used in situations where Pandas is commonly needed, but when Pandas is inadequare due to:
> 
> * Manipulating large datasets, especially when those datasets don’t fit in memory
> * Accelerating long computations by using many cores
> * Distributed computing on large datasets with standard Pandas operations like groupby, join, and time series computations

~~~
import dask.dataframe as dd

dask_dataframe = dd.read_csv('Data/multiTimeline.csv')
help(dd.read_csv)
~~~
{: .language-python}

You can also convert directly from Pandas into Dask!
* there is a low opportunity cost to using Pandas until your data gets too big

~~~
dask_dataframe2 = dd.from_pandas(pandas_dataframe, npartitions=5)

dask_dataframe3 =  dd.from_pandas(pandas_dataframe, chunksize=3)

location = dask_dataframe.loc['2019-07-07', 'Category: All categories']
print(location.compute())

pandas_dataframe.loc['2019-07-07', 'Category: All categories']

print(dask_dataframe.loc['2019-07-07', 'Category: All categories'].compute())

location.compute()

print(dask_dataframe.columns.values)
print(dask_dataframe.index.values)

dask_dataframe.info()

dask_describe = dask_dataframe.describe()
dask_describe.visualize()

dask_describe.compute()
~~~
{: .language-python}

## Dask DataFrames Anti-Uses

Dask DataFrame may not be the best choice in the following situations:

* If your dataset fits into RAM on your laptop, just using Pandas. There are probably simpler ways to improve performance than  parallelism.
* If your dataset doesn’t fit neatly into the Pandas tabular model, then you might find more use in dask.bag or dask.array.
* If you need functions that are not implemented in Dask DataFrame, then you might want to look at dask.delayed which offers more flexibility.
* If you need all of the features that databases offer you should consider PostgresSQL or MySQL.