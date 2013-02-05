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

    def test_all_cv_references(self):
        refs = self.mz5.all_cv_references()
        self.assertEquals(len(refs), 52)
        self.assertEquals(len(refs), 52)
        # Make sure MS id is unique across references
        self.assertEquals(len(set([x[2] for x in refs])), 52)

    def test_cv_reference(self):
        #print self.mz5.get_cv_reference(48)  # ('selected ion m/z', 'MS', 1000744L)
        self.assertEquals(self.mz5.cv_reference(48)[0], 'selected ion m/z')
        self.assertEquals(self.mz5.cv_reference(48)[1], 'MS')
        self.assertEquals(self.mz5.cv_reference(48)[2], 1000744L)
        #    def test_get_cv_param(self):
        # <cvParam cvRef="MS" accession="MS:1000744" name="selected ion m/z" value="367.201873779297" unitCvRef="MS" unitAccession="MS:1000040" unitName="m/z"/>
        # <cvParam cvRef="MS" accession="MS:1000041" name="charge state" value="2"/>
        # <cvParam cvRef="MS" accession="MS:1000042" name="peak intensity" value="302572.5" unitCvRef="MS" unitAccession="MS:1000132" unitName="percent of base peak"/>
        #print self.mz5.get_scan(1).first_ion_params()
        #print self.mz5.get_cv_param(40)  # ('0.8157', 37L, 36L)
        #print self.mz5.get_cv_param(48)  # ('302572.5', 51L, 50L)
        #print self.mz5.get_cv_param(46)  # ('367.201873779297', 48L, 40L)

    def test_psimso_cv_reference_index(self):
        # self.mz5.get_cv_reference(48) => ('selected ion m/z', 'MS', 1000744L)
        self.assertEquals(self.mz5.psimso_cv_reference_index(1000744), 48)

    def test_metadata(self):
        ms1_scan = self.mz5.get_scan(0)
        spectrum_0 = ms1_scan._get_metadata()
        self.assertEquals(spectrum_0.id, "scan=1")
        self.assertEquals(spectrum_0.num_precursors(), 0)
        self.assertEquals(spectrum_0.first_ion_cv_range(), (0, 0))

        ms2_scan = self.mz5.get_scan(1)
        spectrum_1 = ms2_scan._get_metadata()
        self.assertEquals(spectrum_1.id, "scan=2")
        self.assertEquals(spectrum_1.num_precursors(), 1)
        params_1 = ms2_scan.first_ion_cv_params()
        self.assertAlmostEquals(float(params_1[0][0]), 367.201873779297)
        self.assertEquals(float(params_1[1][0]), 2)
        self.assertAlmostEquals(float(params_1[2][0]), 302572.5)

    def test_type_building(self):
        SPECTRUM_TYPE

    def test_open_close(self):
        pass

    #def test_print_sizes(self):
    #    from _mz5_types import print_sizes
    #    print_sizes()
