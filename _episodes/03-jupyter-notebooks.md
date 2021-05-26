---
title: "Jupyter Notebooks"
teaching: 10
exercises: 5
questions:
- "How do Jupyter Notebooks work"
objectives:
- "Gain a basic understanding of Jupyter Notebook operations"
keypoints:
- "Shift-Enter runs cells"
- "Notebooks behave similar to Python scripts, but with a few differences"
- "You need to be careful you are keeping track of the state inside of the notebook"
---

## Jupyter Notebooks - Usage

* Jupyter notebooks, for those of you unfamiliar with python are kind of similar to debugging with VSCode, where you step through code in units at a time.
* To execute code in a cell, press **[Shift + Enter]**.
* Each unit is a cell, and all of the code is executed sequentially inside of the cell.
* State is preserved between cells and cells can be run out of order or run multiple times.

~~~
i = 0
~~~
{: .language-python}

~~~
i += 1
~~~
{: .language-python}

This cell will change value depending on how the above two cells are run.

~~~
print(i)
~~~
{: .language-python}

> ## Jupyter Notebooks - Warnings
> 
> * I cannot reccomend using Jupyter notebooks outside of teaching because of the issues above, and they are slow to execute, heavyweight, and lack many of the features found inside of most IDE's, such as linting and convenient copying and pasting
> * If you want to learn or write python, I reccomend using:
> * **Visual Studio Code** - Full fat IDE with a built in python debugger, can easily be connected to anaconda or other sources of python - My preferred solution to Python on Linux and Windows - [https://code.visualstudio.com/](https://code.visualstudio.com/)
> * **Sublime Text** - Text editor with many plugins to help with linting, code highlighting, etc - Useful for when a full IDE is overkill, such as disposable scripts. - [https://www.sublimetext.com/](https://www.sublimetext.com/)
> * **Vim** - Doesn't really need an introduction, but is very useful when editing code on the command line and has a fairly rich feature set if you spend the time with it. Highly reccomended for interacting with code on the command line, such as our HPC clusters. - Literally every command line interface seems to come bundled with Vim
{: .callout}
