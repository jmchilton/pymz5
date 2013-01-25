# pymz5 - A python library to access [mz5](http://software.steenlab.org/mz5/) mass spectrometry data files.

pymz5 is built on top of the h5py python library for accessing HDF5
data format (of which mz5 is a specific
implementation). Traditionally, python libraries that build on each
other via dependencies, but due to complexities related Cython
compliation pymz5 is a direct fork of h5py.

The README for h5py can be found [here](h5py_README.txt).

Initially this library will focus on functionality required for
visualization, but feel free to submit a [feature
request](https://github.com/jmchilton/pymz5/issues/new) or issue a
[pull request](https://github.com/jmchilton/pymz5/pulls).

## Requirements

Building pymz5 requires:

  * HDF5 1.8.3 or later on Linux (h5py supports Windows, but pymz5 considers this unsupported though it likely works)
  * Python 2.7 or 3.2
  * Any modern version of NumPy
  * Cython 0.13 or later, to build from a git checkout

## Building

Build and test and install pymz5:

    $ git clone https://github.com/jmchilton/pymz5 
    $ cd pymz5/h5py
    $ python api_gen.py
    $ cd ..
    $ python setup.py build [--hdf5=/path/to/hdf5]
    $ python setup.py test
    $ [sudo] python setup.py install

