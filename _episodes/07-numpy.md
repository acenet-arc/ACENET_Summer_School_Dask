---
title: "Numpy"
teaching: 10
exercises: 5
questions:
- "What is Numpy?"
- "Why use Numpy?"
objectives:
- "Learn the basics of Numpy and Numy Arrays so we can understand Dask Arrays"
keypoints:
- "Numpy is a very fast python package, written in C that can do most of your math problems"
- "Numpy is great for dealing with high-dimensional data"
- "Numpy is the preferred data-loader for a lot of machine-learning frameworks"
---


## Numpy

![](../fig/Math.jpg)
* Numpy is a widely used and comprehensive mathematics package in python
* Numpy stands for "Numerical Python", and handles tasks such as matrix math, trig, linear algebra, etc.
* Is very useful for matrix math, and matrix-like operations, such as loading data into machine learning algorithms
* This talk will not deep-dive into numpy, but will instead talk about a few key features, give a rough idea of what numpy is capable of, before moving on to dask arrays

~~~
import numpy as np
~~~
{: .language-python}

* Numpy primarily works on arrays of data, though several functions can be called on intigers or floats.
* Arrays may have between 1 and n dimensions, and are primarily limited in size by the amount of ram a computer has to operarte on them.
* We will walk through a quick example on how to create a numpy arrray, then pass it over to DASK

~~~
array = np.arange(16)
print(array)

array_square = array.reshape(4,4)
print(array_square)

print(array.shape)
print(array_square.shape) 
~~~
{: .language-python}

## Numpy 
* Numpy backs onto well-written, compiled software, so it performs faster and more reliable calculations than most code you can write yourself
* Numpy has most of the mathematical functions that one could ask for, a non-exhaustive list includes

|Function          | Description |
|------------------|-------------------------------------------------------------------------|
| tan()            | Compute tangent element-wise.|
| arcsin()         | Inverse sine, element-wise.|
| arccos()         | Trigonometric inverse cosine, element-wise.|
| arctan()         | Trigonometric inverse tangent, element-wise.|
| arctan2()        | Element-wise arc tangent of x1/x2 choosing the quadrant correctly.|
| degrees()        | Convert angles from radians to degrees.|
| rad2deg()        | Convert angles from radians to degrees.|
| deg2rad          | Convert angles from degrees to radians.|
| radians()        | Convert angles from degrees to radians.|
| hypot()          | Given the “legs” of a right triangle, return its hypotenuse.|
| unwrap()         | Unwrap by changing deltas between values to 2*pi complement.|
| rint()           | Round to nearest integer towards zero.|
| fix()            | Round to nearest integer towards zero.|
| floor()          | Return the floor of the input, element-wise.|
| ceil()           | Return the ceiling of the input, element-wise.|
| trunc()          | Return the truncated value of the input, element-wise.|
| expm1()          | Calculate exp(x) – 1 for all elements in the array.|
| exp2()           | Calculate `2**p` for all `p` in the input array.|
| log10()          | Return the base 10 logarithm of the input array, element-wise|
| log2()           | Base-2 logarithm of x.|
| log1p()          | Return the natural logarithm of one plus the input array, element-wise.|
| logaddexp()      | Logarithm of the sum of exponentiations of the inputs.|
| logaddexp2()     | Logarithm of the sum of exponentiations of the inputs in base-2.|
| convolve()       | Returns the discrete, linear convolution of two one-dimensional sequences.|
| sqrt()           | Return the non-negative square-root of an array, element-wise.|
| square()         | Return the element-wise square of the input.|
| absolute()       | Calculate the absolute value element-wise.|
| fabs()           | Compute the absolute values element-wise.|
| sign()           | Returns an element-wise indication of the sign of a number.|
| interp()         | One-dimensional linear interpolation.|
| maximum()        | Element-wise maximum of array elements.|
| minimum()        | Element-wise minimum of array elements.|
| real_if_close()  | If complex input returns a real array if complex parts are close to zero.|
| nan_to_num()     | Replace NaN with zero and infinity with large finite numbers.|
| heaviside()      | Compute the Heaviside step function.|

~~~
print(np.square(array))
print(np.sqrt(array_square))
~~~
{: .language-python}

The biggest reason to use numpy, however is that it allows your data to be used by various other frameworks, such as...
![](../fig/Scikit_learn_logo.svg)
![](../fig/TensorFlowLogo.png)
![](../fig/Pytorch_logo.png)
