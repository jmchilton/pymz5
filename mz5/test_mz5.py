from os.path import join
from unittest import TestCase

from mz5 import Mz5
from mz5 import SPECTRUM_TYPE
from h5py import h5o



class Mz5Test(TestCase):

    def setUp(self):
        path = join("test_data", "test.mz5")
        self.mz5 = Mz5(path)
        self.mz5.open()

    def tearDown(self):
        self.mz5.close()

    def test_range(self):
        # print self.mz5._spectrum_index()[:]
        self.assertEquals(len(self.mz5._spectrum_index()), 26)
        (start, end) = self.mz5._get_offset_range(0)
        self.assertEquals(start, 0)
        self.assertEquals(end, 1480)

        (start, end) = self.mz5._get_offset_range(25)
        self.assertEquals(start, 21659)
        self.assertEquals(end, len(self.mz5._spectrum_intensity()))

    def test_get_peaks(self):
        ms2_scan = self.mz5.get_scan(1)
        mzs = ms2_scan.get_mzs()
        intensities = ms2_scan.get_intensities()
        self.assertEquals(len(mzs), 239)
        self.assertEquals(len(intensities), 239)
        self.assertAlmostEqual(mzs[0], 112.0870743, 3)
        self.assertAlmostEqual(intensities[0], 3164.949463, 3)
        self.assertAlmostEqual(mzs[238], 591.2958984, 3)
        self.assertAlmostEqual(intensities[238], 199.230423, 3)

    def test_get_cv_param(self):
        print self.mz5.get_cv_reference(48)
        print self.mz5.get_cv_param(40)
        print self.mz5.get_cv_param(48)
        print self.mz5.get_cv_param(46)

    def test_metadata(self):
        spectrum_0 = self.mz5.get_scan_metadata(0)
        self.assertEquals(spectrum_0.id, "scan=1")
        self.assertEquals(spectrum_0.num_precursors(), 0)
        self.assertEquals(spectrum_0.first_ion_params(), (0, 0))

        spectrum_1 = self.mz5.get_scan_metadata(1)
        self.assertEquals(spectrum_1.id, "scan=2")
        self.assertEquals(spectrum_1.num_precursors(), 1)
        self.assertEquals(spectrum_1.first_ion_params(), (46, 49))

    def test_type_building(self):
        SPECTRUM_TYPE

    def test_open_close(self):
        pass

    #def test_print_sizes(self):
    #    from _mz5_types import print_sizes
    #    print_sizes()
