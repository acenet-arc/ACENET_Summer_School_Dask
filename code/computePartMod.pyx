cpdef long long computePart(int size):
  cdef long long part=0
  cdef int i
  for i in range(size):
    part=part+i
  return part

