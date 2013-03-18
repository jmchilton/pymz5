from defs cimport *

## Metadata data structures

cdef struct ParamList:
    unsigned long cvParamStartID
    unsigned long cvParamEndID
    unsigned long userParamStartID
    unsigned long userParamEndID
    unsigned long refParamGroupStartID
    unsigned long refParamGroupEndID

cdef struct Ref:
    unsigned long refID

cdef struct ParamLists:
    size_t len
    ParamList* lists

cdef struct Precursor:
    char* externalSpectrumId
    ParamList activation
    ParamList isolationWindow
    ParamLists selectedIonList
    Ref spectrumRefID
    Ref sourceFileRefID

cdef struct Scan:
    char* externalSpectrumID
    ParamList paramList
    ParamLists scanWindowList
    Ref instrumentConfigurationRefID
    Ref sourceFileRefID
    Ref spectrumRefID

cdef struct PrecursorList:
    size_t len
    Precursor* list

cdef struct ScanList:
    size_t len
    Scan* list

cdef struct Scans:
    ParamList paramList
    ScanList scanList

cdef struct SpectrumStruct:
    char* id
    char* spotID
    ParamList paramList
    Scans scanList
    PrecursorList precursorList
    ParamLists productList
    Ref dataProcessingRefID
    Ref sourceFileRefID
    unsigned int index

ctypedef SpectrumStruct* Spectrum_ptr

## Other Data Structures

cdef struct CVParam:
    char value[128]
    unsigned long typeCVRefID
    unsigned long unitCVRefID

cdef struct ProcessingMethodList:
    size_t len
    ProcessingMethod* list

cdef struct DataProcessing:
    char* id
    ProcessingMethodList processingMethodList

cdef struct ProcessingMethod:
    ParamList paramList
    Ref softwareRefID
    unsigned long order

