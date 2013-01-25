from defs cimport *

cdef struct CVParamMZ5:
    char value[128]
    unsigned long typeCVRefID
    unsigned long unitCVRefID

cdef struct ParamListMZ5Data:
    unsigned long cvParamStartID
    unsigned long cvParamEndID
    unsigned long userParamStartID
    unsigned long userParamEndID
    unsigned long refParamGroupStartID
    unsigned long refParamGroupEndID

cdef struct ParamListsMZ5:
    size_t len
    ParamListMZ5Data* lists

cdef struct RefMZ5Data:
    unsigned long refID

cdef struct ProcessingMethodMZ5:
    ParamListMZ5Data paramList
    RefMZ5Data softwareRefID
    unsigned long order

cdef struct ProcessingMethodListMZ5:
    size_t len
    ProcessingMethodMZ5* list

cdef struct DataProcessingMZ5:
    char* id
    ProcessingMethodListMZ5 processingMethodList

cdef struct ScanMZ5:
    char* externalSpectrumID
    ParamListMZ5Data paramList
    ParamListsMZ5 scanWindowList
    RefMZ5Data instrumentConfigurationRefID
    RefMZ5Data sourceFileRefID
    RefMZ5Data spectrumRefID

cdef struct ScanListMZ5:
    size_t len
    ScanMZ5* list

cdef struct ScansMZ5:
    ParamListMZ5Data paramList
    ScanListMZ5 scanList

cdef struct PrecursorMZ5:
    char* externalSpectrumId
    ParamListMZ5Data activation
    ParamListMZ5Data isolationWindow
    ParamListsMZ5 selectedIonList
    RefMZ5Data spectrumRefID
    RefMZ5Data sourceFileRefID

cdef struct PrecursorListMZ5:
    size_t len
    PrecursorMZ5* list

cdef struct SpectrumMZ5:
    char* id
    char* spotID
    ParamListMZ5Data paramList
    ScansMZ5 scanList
    PrecursorListMZ5 precursorList
    ParamListsMZ5 productList
    RefMZ5Data dataProcessingRefID
    RefMZ5Data sourceFileRefID
    unsigned int index

ctypedef SpectrumMZ5* SpectrumMZ5_ptr


