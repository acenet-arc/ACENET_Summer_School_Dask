cpdef double sumnum(int n):
  cdef double result=0.0
  cdef int i
  for i in range(n):
    result+=i
  return result

