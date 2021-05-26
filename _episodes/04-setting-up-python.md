---
title: "Setting up Python"
teaching: 5
exercises: 10
questions:
- "How to set up Python"
objectives:
- "Set up Jupyter and Python"
keypoints:
- "Loading Python Modules"
- "Setting up virtual environment"
- "Connecting virtual environment to Jupyter"
---


## Setting up Python

* To do python on the clusters, we use a virtual environment.
* To create and load into a virtual environment, enter these commands in your terminal

~~~
$ module load python/3.7
$ module load scipy-stack
$ virtualenv --no-download ~/Parallel_Tutorial
$ source ~/Parallel_Tutorial/bin/activate
~~~
{: .language-bash}

* To deactivate the environment enter in "deactivate", and you should be back to the normal bash terminal.
* Now that the environment exists, we can install some python packages using python's package manager, pip [Pip Installs Python]
* There are several ways to do this, but the packages that we require are: Scikit-Learn, DASK, Graphviz, Numpy, Pandas and MatPlotLib
* Scipy stack takes care of most of that for us, installing Numpy Pandas, and MatPlotLib. (thanks, sysadmins!)

~~~
$ pip install --no-index --upgrade pip
$ pip install --no-index dask
$ pip install --no-index scikit-learn
$ pip install toolz
$ pip install graphviz 
~~~
{: .language-bash}
