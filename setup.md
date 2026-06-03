---
title: Setup
---

We will be working on a Digital Research Alliance of Canada (the Alliance) high performance compute (HPC) or virtual cluster with all the tools we will need already installed. You will need a method of connecting to either an Alliance cluster, or our virtual cluster, which means you will need a method of connecting to them using [SSH](https://docs.alliancecan.ca/wiki/SSH). SSH can be used from a terminal which we explain how to install and open in the **Ensure you can open a terminal** section below.

# Virtual training cluster
We provide a virtual training cluster called a "Magic Castle" for doing exercises and playing with example code. Using the Magic Castle means you and all the other students will have the same environment, which means easier troubleshooting when things go wrong--- which they sometimes do. The Magic Castle will be destroyed at the end of the course, so you don't need to worry about messing up your work environment and you can experiment freely. 

# Alliance Account
If you already have an Alliance account and access to any Alliance HPC cluster, you can log into it to follow along. If you use your Alliance account you'll be able to continue to play with the example code even after the workshop has ended and we've destroyed the Magic Castle. 

# Ensure you can open a terminal
The only setup required on your laptop is ensuring you can open an SSH terminal.

### Windows
You can use Windows PowerShell or Windows Cmd tool if your Windows version is not too old.  Open either one and type `ssh -V`.  You should see a response something like "OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2".  The precise version doesn't matter, so long as it isn't too old.

If you have a very old version of Windows or if you get an error from `ssh -V`, then we recommend [MobaXterm](http://mobaxterm.mobatek.net/). Download and install MobaXterm **home installer edition**. Once you have MobaXterm installed, start it and then "start local terminal" therein.

### Mac/Linux
You already have a terminal built in.

To see how to open your terminal on your **Mac** see this [youtube video](https://www.youtube.com/watch?v=zw7Nd67_aFw).

If you are a **Linux** user running Ubuntu, you should be able to press the `ctrl`+`alt`+`T` keys to open a terminal. Alternatively the first 30 seconds of this [youtube video](https://www.youtube.com/watch?v=_xUvH2iRizU) shows you how to access the terminal on Ubuntu 14. If you are having trouble accessing a terminal on your laptop before you arrive we can help you at the beginning of the workshop.

# Optional, setup X11
If possible it would also be nice to have a means of running an X11 server on your local machine. This will allow you to see some figures that are generated during the lesson, however it is not strictly required. 
+ On **Windows** if you use [MobaXTerm](https://mobaxterm.mobatek.net/) to connect via `ssh` it has a built in x11 server.
+ On **Macs** you may need to install the [XQuartz](https://www.xquartz.org/) application.
+ On **Linux** you should already be set.


# Test your ssh connection

### If using our virtual cluster
To connect to our virtual training cluster, follow the instructions given in the "Magic Castle Username and Password" item on the course page, or follow the course instructor's guidance in the first few minutes of the course.

### If using an Alliance account
If you are using your Alliance account make sure you can connect to an Alliance cluster. To connect to the Nibi cluster for example you would use the command below.
~~~
$ ssh nibi.alliancecan.ca
~~~
{: .bash}

{% include links.md %}
