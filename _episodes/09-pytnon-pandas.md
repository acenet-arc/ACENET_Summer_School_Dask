---
title: "Python - Pandas"
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

## Python - Pandas

![](../fig/Panda.jpg)

* Pandas is effectively a spreadsheeting program for python, running on Python/Cython/C with a Python front-end.
* Pandas is similar to Excel, but does not have a GUI, so it is faster, but less user friendly.
* Pandas tends to operate more quickly and efficiently than full-fat Microsoft Excel.
* Pandas operates primarily using DataFrames, rougly equivalent to Excel Sheets.

**The data is the google search trends for the word "parallel"**

~~~
import pandas as pd

pandas_dataframe = pd.read_csv('Data/multiTimeline.csv')
print(pandas_dataframe.head())
~~~
{: .language-python}

Pandas offers much of the same functionality as Excel, except you need to print out data to the terminal to see it.

~~~
print(pandas_dataframe.columns.values)
print(pandas_dataframe.index.values)
~~~
{: .language-python}

You can print out data from a specific locus or from a pair of headings

~~~
print(pandas_dataframe.iloc[5, 0])
print(pandas_dataframe.loc['2019-07-07', 'Category: All categories'])
~~~
{: .language-python}

You can get a dump of the information about a dataframe, such as what it contains and the datatypes stored inside of it.

~~~
print(pandas_dataframe.info())
~~~
{: .language-python}

You can also have pandas crunch bulk statistics on your data.

~~~
pandas_dataframe.describe()
~~~
{: .language-python}

You can also perform excel functions/operations on data such as plotting using packages like matplotlib.

~~~
%matplotlib inline
import matplotlib.pyplot as plt

print(pandas_dataframe.iloc[1:,0])
print(type(pandas_dataframe.iloc[1,0])) 

pandas_dataframe.iloc[1:,0] = pandas_dataframe.iloc[1:,0].astype(int)
print(type(pandas_dataframe.iloc[1,0]))

pandas_dataframe.iloc[1:,0].plot()
~~~
{: .language-python}