from _mz5_helpers cimport get_object

cdef class Spectrum:
    cdef Spectrum_ptr ptr

    def __cinit__(self):
        pass

    def __dealloc__(self):
        cdef Spectrum_ptr spectrum = self.ptr
        if spectrum is not NULL:
            self.dealloc_param_lists(spectrum.productList)
            self.dealloc_scan_list(spectrum.scanList.scanList)
            self.dealloc_precursor_list(spectrum.precursorList)
            free(spectrum.spotID)
            free(spectrum.id)
            free(spectrum)

    cdef dealloc_precursor_list(self, PrecursorList obj):
        cdef int i = 0
        cdef Precursor precursor
        while i < obj.len:
            precursor = obj.list[i]
            free(precursor.externalSpectrumId)
            self.dealloc_param_lists(precursor.selectedIonList)
            i += 1
        free(obj.list)

    cdef dealloc_scan_list(self, ScanList obj):
        cdef int i = 0
        cdef Scan scan
        while i < obj.len:
            scan = obj.list[i]
            free(scan.externalSpectrumID)
            self.dealloc_param_lists(scan.scanWindowList)
            i += 1
        free(obj.list)

    cdef dealloc_param_lists(self, ParamLists obj):
        cdef ParamList* list
        free(obj.lists)

    def num_precursors(self):
        return self.ptr.precursorList.len

    def num_ions(self):
        cdef Precursor precursor
        cdef PrecursorList precursorList = self.ptr.precursorList
        if precursorList.len < 1:
            return 0
        else:
            precursor = precursorList.list[0]
            return precursor.selectedIonList.len


    def first_ion_cv_range(self):
        cdef ParamList* params = self.first_selected_ion()
        if params is NULL:
            return (0, 0)
        cdef ParamList param = params[0]
        return (param.cvParamStartID, param.cvParamEndID)

    cdef ParamList* first_selected_ion(self):
        cdef Precursor precursor
        cdef ParamLists selectedIonList
        cdef PrecursorList precursorList = self.ptr.precursorList
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
    print sizeof(ParamList)
    print sizeof(Scan)
    print sizeof(Scans)
    print sizeof(Ref)
    print sizeof(Precursor)

def populate_spectrum_metadata(dset_id, type_id, index, Spectrum spectrum):
    spectrum.ptr = <Spectrum_ptr>get_object(dset_id, type_id, index)
    return spectrum
