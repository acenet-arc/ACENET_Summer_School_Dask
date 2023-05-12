---
title: Setup
---

The exercises in this lesson will be carried out on the virtual cluster we have setup for this workshop and we will provide login information at the beginning of the lesson. If you have an Alliance account, you should be able to follow along on any of the [Alliance general-purpose clusters](https://docs.alliancecan.ca/wiki/National_systems#Compute_clusters) (Béluga, Cedar, Graham, Narval). However, you may need to wait for jobs to schedule depending on your usage history and how busy the clusters are. Therefore using the virtual cluster is still preferred for this lesson.

Make sure you have a means of connecting via `ssh` to a remote cluster.
+ On **Windows** [MobaXTerm](https://mobaxterm.mobatek.net/) is a good option.
+ On **Mac** and **Linux** machines there is a built in *terminal* application that you can use similarly to how Windows users will use MobaXTerm.

If possible it would also be nice to have a means of running an X11 server on your local machine. This will allow you to see some figures that are generated during the lesson, however it is not strictly required. 
+ On **Windows** if you use [MobaXTerm](https://mobaxterm.mobatek.net/) to connect via `ssh` it has a built in x11 server.
+ On **Macs** you may need to install the [XQuartz](https://www.xquartz.org/) application.
+ On **Linux** you should already be set.

<!--
~~~
$ module load python/3.8
$ module load scipy-stack
$ virtualenv --no-download ~/Parallel_Tutorial (takes some time, maybe 1-2 mins)
$ source ~/Parallel_Tutorial/bin/activate
$ pip install --no-index --upgrade pip (takes some time, maybe 1 min)
$ pip install --no-index dask
$ pip install --no-index scikit-learn
$ pip install toolz
$ pip install graphviz
$ pip install --no-index distributed 
~~~
{: .bash}

Note about the slides …
They are in a Jupyter notebook.

[https://github.com/MatACENET/Dask-Tutorial](https://github.com/MatACENET/Dask-Tutorial)
-->
{% include links.md %}
