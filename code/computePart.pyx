cpdef int computePart(int size):
  cdef int part=0
  cdef int i
  for i in range(size):
    part=part+i
  return part

