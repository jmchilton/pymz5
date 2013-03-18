from os.path import join
from unittest import TestCase
from resource import getrusage, RUSAGE_SELF
from mz5 import Mz5

TEST_MEMORY = False
PRINT_FREQUENCY = 100


class TestMemory(TestCase):

    def test_memory(self):
        iteration = 0
        while TEST_MEMORY:
            iteration += 1
            path = join("test_data", "test.mz5")
            mz5 = Mz5(path)
            mz5.open()
            for index in range(len(mz5)):
                mz5.get_scan(index).first_ion_cv_params()
                continue
            mz5.close()
            if (iteration % PRINT_FREQUENCY) == 0:
                print "Iteration %d, memory usage %d" % \
                    (iteration, getrusage(RUSAGE_SELF).ru_maxrss)
