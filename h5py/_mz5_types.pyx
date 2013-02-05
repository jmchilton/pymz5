from _mz5_helpers cimport get_object

cdef class Spectrum:
    cdef SpectrumMZ5_ptr ptr

    def __cinit__(self):
        pass

    def __dealloc__(self):
        if self.ptr is not NULL:
            free(self.ptr)

    def num_precursors(self):
        return self.ptr.precursorList.len

    def num_ions(self):
        cdef PrecursorMZ5 precursor
        cdef PrecursorListMZ5 precursorList = self.ptr.precursorList
        if precursorList.len < 1:
            return 0
        else:
            precursor = precursorList.list[0]
            return precursor.selectedIonList.len


    def first_ion_cv_range(self):
        cdef ParamListMZ5Data* params = self.first_selected_ion()
        if params is NULL:
            return (0, 0)
        cdef ParamListMZ5Data param = params[0]
        return (param.cvParamStartID, param.cvParamEndID)

    cdef ParamListMZ5Data* first_selected_ion(self):
        cdef PrecursorMZ5 precursor
        cdef ParamListsMZ5 selectedIonList
        cdef PrecursorListMZ5 precursorList = self.ptr.precursorList
        if precursorList.len < 1:
            return NULL
        
        precursor = precursorList.list[0]
        selected_ion_list = precursor.selectedIonList
        if selected_ion_list.len < 1:
            return NULL

        return &selected_ion_list.lists[0]


    property id:
        def __get__(self):
            ptr = self.ptr
            return self.ptr[0].id

def print_sizes():
    print sizeof(ParamListMZ5Data)
    print sizeof(ScanMZ5)
    print sizeof(ScansMZ5)
    print sizeof(RefMZ5Data)
    print sizeof(PrecursorMZ5)

def populate_spectrum_metadata(dset_id, type_id, index, Spectrum spectrum):
    spectrum.ptr = <SpectrumMZ5_ptr>get_object(dset_id, type_id, index)
    return spectrum
