from h5py.h5t import TypeStringID, typewrap
from h5py.h5t cimport TypeID


from utils cimport emalloc
from _objects cimport pdefault

cdef object lockid(hid_t id_in):
    cdef TypeID tid
    tid = typewrap(id_in)
    tid.locked = 1
    return tid

NATIVE_ULONG = lockid(H5T_NATIVE_ULONG)

cpdef c_vlen_str():
    # Variable-length strings
    cdef hid_t tid
    tid = H5Tcopy(H5T_C_S1)
    H5Tset_size(tid, H5T_VARIABLE)
    return TypeStringID(tid)



cdef void read_object(dset_id, type_id, index, void* buffer):
    cdef hssize_t coord[1][1]
    cdef hsize_t marray[1]
    marray[0] = 1
    coord[0][0] = index

    memspace = H5Screate_simple (1, marray, NULL)
    dataspace = H5Dget_space(dset_id)
    ret = H5Sselect_elements(dataspace, H5S_SELECT_SET, 1, <hsize_t **> coord)
    if ret < 0:
        raise Exception("H5Sselect_elements failed")
    ret = H5Dread(dset_id, type_id, memspace, dataspace, pdefault(None), <void *>buffer)
    if ret < 0:
        raise Exception("H5Dread failed")

    H5Sclose(dataspace)
    H5Sclose(memspace)

cdef void* get_object(hid_t dset_id, hid_t type_id, int index):
    cdef hsize_t dtype_size = H5Tget_size(type_id)
    cdef void* buf = <void*>emalloc(dtype_size)
    read_object(dset_id, type_id, index, <void *>buf)
    return buf


