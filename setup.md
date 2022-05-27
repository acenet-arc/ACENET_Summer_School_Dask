---
title: Setup
---

The exercises in this lesson will be carried out on the virtual cluster we have been using the rest of the course, `pcs.ace-net.training.` If you have a Compute Canada account, you should be able to follow along equally well on any of the Compute Canada general-purpose clusters (Béluga, Cedar, Graham).

Make sure you have a means of connecting via `ssh` to a remote cluster. On windows [MobaXTerm](https://mobaxterm.mobatek.net/) is a good option. On Mac and Linux machines there is a built in *terminal* application that you can use similarly to how Windows users will use MobaXTerm.

If possible it would also be nice to have a means of running an x11 server. This will allow you to see some figures that are generated during the workshop, however it is not strictly required. On windows if you use [MobaXTerm](https://mobaxterm.mobatek.net/) to connect via `ssh` it has a built in x11 server. On Macs you may need to install the [XQuartz](https://www.xquartz.org/) application.

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
