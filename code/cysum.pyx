cpdef float sumnum(int n):
  cdef float result=0.0
  cdef int i
  for i in range(n):
    result+=float(i)
  return result

