---
title: "Python - General"
teaching: 10
exercises: 5
questions:
- "What's python?"
- "How do I use Python?"
objectives:
- "Learn the absolute basics of python"
keypoints:
- "Variable = content"
- "List = [content, content, content]"
- "Functions"
- "For Loops"
- "Import Statements"
---

## Python - General

Python is an interperted software language that has a great deal of support in scientific and mathematical computing

* The major packages we will be referencing are Numpy, Pandas and of course Dask
Variables are assigned using

#Variables
~~~
variable_name = variable_content
~~~
{: .language-python}

* Variables may not start with a number
* May only contain underscores and alphanumeric characters
* Are case-sensitive
     
# Lists     
Lists are created in python using 

~~~
list_name = [var_1, var_2, ... var_n]
~~~
{: .language-python}

# Functions
* Functions are created using 

~~~
def function_name(arg_1, arg_2, ... arg_n):
    code_goes_here
~~~
{: .language-python}

* Functions are called using 

~~~
function_name(arg_1, arg_2, ... arg_n)
~~~
{: .language-python}

# For Loops
* For loops are created using

~~~
for object in iterator:
    code_goes_here
~~~
{: .language-python}

* Loop and function scope is indicated by indentation depth
* Colons are used to indicate a for loop or function has been defined.

~~~
for i in range(0,5):
    print(i*2)
~~~
{: .language-python}

# Importing Libraries

* Functions and libraries are imported using

~~~
import package_name**
~~~
{: .language-python}

or

~~~
from package_name import sub_package
~~~
{: .language-python}

* How functions from libraries are used:

~~~
package_name.sub_package(args)
~~~
{: .language-python}

or
~~~
sub_package(args)
~~~
{: .language-python}
