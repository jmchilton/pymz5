from h5py import File
from h5py import h5t

from numpy import cumsum

from h5py._mz5_helpers import c_vlen_str, NATIVE_ULONG
from h5py._mz5_types import populate_spectrum_metadata
from h5py._mz5_types import Spectrum

# mz5 keys:
# [u'CVParam', u'CVReference', u'ControlledVocabulary', u'DataProcessing',
# u'FileContent', u'FileInformation', u'InstrumentConfiguration', u'Run',
# u'Samples', u'Software', u'SourceFiles', u'SpectrumIndex', u'SpectrumIntensity',
# u'SpectrumListBinaryData', u'SpectrumMZ', u'SpectrumMetaData', u'UserParam']

SPECTRUM_MZ5_SIZE = 184
PARAM_LIST_MZ5_SIZE = 48
SCANS_MZ5_SIZE = 64
SCAN_MZ5_SIZE = 96
REF_MZ5_SIZE = 8
PRECURSOR_MZ5_SIZE = 136


def _build_spectrum_type():
    type = CompoundType(SPECTRUM_MZ5_SIZE)
    type.insert("id", c_vlen_str())
    type.insert("spotID", c_vlen_str())
    type.insert("params", build_param_list_mz5_type())
    type.insert("scans", build_scans_list_mz5_type())
    type.insert("precursors", build_precursor_list_mz5_type())
    type.insert("products", build_param_lists_mz5_type())
    type.insert("refDataProcessing", build_ref_mz5_type())
    type.insert("refSourceFile", build_ref_mz5_type())
    type.insert("index", NATIVE_ULONG)
    type.lock()
    return type


def build_precursor_list_mz5_type():
    return _vlen_type(build_precursor_mz5_type())


def build_precursor_mz5_type():
    type = CompoundType(PRECURSOR_MZ5_SIZE)
    type.insert("externalSpectrumId", c_vlen_str())
    type.insert("activation", build_param_list_mz5_type())
    type.insert("isolationWindow", build_param_list_mz5_type())
    type.insert("selectedIonList", build_param_lists_mz5_type())
    type.insert("refSpectrum", build_ref_mz5_type())
    type.insert("refSourceFile", build_ref_mz5_type())
    type.lock()
    return type


def build_param_list_mz5_type():
    type = CompoundType(PARAM_LIST_MZ5_SIZE)
    long_type = NATIVE_ULONG
    type.insert("cvstart", long_type)
    type.insert("cvend", long_type)
    type.insert("usrstart", long_type)
    type.insert("usrend", long_type)
    type.insert("refstart", long_type)
    type.insert("refend", long_type)
    type.lock()
    return type


def build_scan_list_mz5_type():
    return _vlen_type(build_scan_mz5_type())


def build_param_lists_mz5_type():
    return _vlen_type(build_param_list_mz5_type())


def _vlen_type(type):
    vtype = h5t.vlen_create(type.type_id)
    return vtype


def build_ref_mz5_type():
    type = CompoundType(REF_MZ5_SIZE)
    long_type = NATIVE_ULONG
    type.insert("refID", long_type)
    type.lock()
    return type


def build_scan_mz5_type():
    type = CompoundType(SCAN_MZ5_SIZE)
    type.insert("externalSpectrumID", c_vlen_str())
    type.insert("params", build_param_list_mz5_type())
    type.insert("scanWindowList", build_param_lists_mz5_type())
    type.insert("refInstrumentConfiguration", build_ref_mz5_type())
    type.insert("refSourceFile", build_ref_mz5_type())
    type.insert("refSpectrum", build_ref_mz5_type())
    type.lock()
    return type


def build_scans_list_mz5_type():
    type = CompoundType(SCANS_MZ5_SIZE)
    params = build_param_list_mz5_type()
    type.insert("params", params)
    type.insert("scanList", build_scan_list_mz5_type())
    type.lock()
    return type


class CompoundType(object):

    def __init__(self, size):
        self.type_id = h5t.create(h5t.COMPOUND, size)
        self.offset = 0

    def insert(self, name, type_or_id):
        if isinstance(type_or_id, CompoundType):
            type_id = type_or_id.type_id
        else:
            type_id = type_or_id
        size = type_id.get_size()
        offset = self.offset
        self.type_id.insert(name, offset, type_id)
        self.offset = offset + size

    def lock(self):
        self.type_id.lock()

    def raw_id(self):
        return self.type_id.id

SPECTRUM_TYPE = _build_spectrum_type()


class Mz5(object):
    """ High-level interface to mz5 files
    """

    def __init__(self, path):
        self.path = path
        self.f = None

    def open(self):
        self.f = File(self.path)

    def close(self):
        self.f.close()
        self.f = None

    def _spectrum_index(self):
        return self.f['SpectrumIndex']

    def _spectrum_intensity(self):
        return self.f['SpectrumIntensity']

    def _spectrum_mz(self):
        return self.f['SpectrumMZ']

    def _spectrum_metadata(self):
        return self.f['SpectrumMetaData']

    def _get_offset_range(self, scan_index):
        previous_index = max(scan_index - 1, 0)
        result = self._spectrum_index()[previous_index:(scan_index + 1)]
        if len(result) == 2:
            return (result[0], result[1])
        else:
            return (0, result[0])

    def get_scan(self, scan_index):
        return Scan(self, scan_index)

    def get_scan_metadata(self, index):
        spectrum = Spectrum()
        dset = self._spectrum_metadata()
        populate_spectrum_metadata(dset.id.id, SPECTRUM_TYPE.raw_id(), index, spectrum)
        return spectrum

    def all_cv_references(self):
        return self.f['CVReference'][:]

    def cv_reference(self, hdf5_index):  # HDF5 index, second number inf CVParam tuple
        if not hasattr(self, 'cv_reference_dict'):
            self.cv_reference_dict = dict(enumerate(self.all_cv_references()))
        return self.cv_reference_dict[hdf5_index]

    def psimso_cv_reference_index(self, psimso_id):
        """
        Takes in a Proteomics Standards Initiative Mass Spectrometry Ontology
        identifier (psimso_id) and returns the HDF5 CV reference index for that
        identifier.
        """
        if not hasattr(self, 'psimso_index_dict'):
            # TODO: This hardcodes that MS is the prefix for PSI MSO data
            # should probably pull this information from 'ControllerVocabulary'
            self.psimso_index_dict = dict([(ref[2], i) for (i, ref) in enumerate(self.all_cv_references()) if ref[1] == 'MS'])
        return self.psimso_index_dict[psimso_id]


class Scan(object):

    def __init__(self, mz5, scan_index):
        self.mz5 = mz5
        self.scan_index = scan_index

    def _offeset_range(self):
        if not hasattr(self, 'offset_range'):
            self.offset_range = self.mz5._get_offset_range(self.scan_index)
        return self.offset_range

    def get_intensities(self):
        (start, end) = self._offeset_range()
        return self.mz5._spectrum_intensity()[start:end]

    def get_mzs(self, cumulative=True):
        (start, end) = self._offeset_range()
        # mz array comes in as first m/z value and then deltas so
        # compute the cumulative sumation of this.
        raw_mzs = self.mz5._spectrum_mz()[start:end]
        return cumsum(raw_mzs) if cumulative else raw_mzs

    def _get_metadata(self):
        if hasattr(self, 'metadata'):
            return self.metadata
        else:
            metadata = self.mz5.get_scan_metadata(self.scan_index)
            self.metadata = metadata
            return metadata

    def first_ion_cv_params(self):
        metadata = self._get_metadata()
        params = metadata.first_ion_cv_range()
        ref_start = params[0]
        ref_end = params[1]
        #print ref_start
        #print ref_end
        #print params[4], params[5]
        return self.mz5.f['CVParam'][ref_start:ref_end]


#from h5py.h5s import ALL
#from h5py import h5o
    #return self._read_doubles('/SpectrumIntensity', start, end)
    #return self._read_doubles('/SpectrumMZ', start, end)

    #def _read_doubles(self, path, start, end):
    #    g = h5o.open(self.mz5.f.fid, path)
    #    data_read_bytes = zeros((end - start), dtype=dtype('S124'))
    #    g.read(ALL, ALL, data_read_bytes, mtype=g.get_type())
    #    return data_read_bytes
