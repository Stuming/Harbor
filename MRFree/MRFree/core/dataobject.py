import numpy as np
import nibabel as nib
from sklearn.cluster import SpectralClustering


class Region(Object):
    def __init__(self, name=None):
        self.name = name
        self.region_size = None
        self.data = dict(Geometry=None, Morphology=None, Function=None, Tract=None, Network=None, Gene=None)

    def load_data(self, datatype, para):
        # This method is a general designation, should be expanded. Data can be anatomy, scalar, tract...
        self.data[datatype].load_data(para)

    def save_data(self, datatype, para):
        self.data[datatype].save_data(para)

    def get_property(self, datatype, propertyname):
        # This method is a general designation, should be expanded. Property can be name, id, space...
        return self.data[datatype].get_property(propertyname)

    def set_property(self, datatype, propertyname):
        self.data[datatype].set_property(propertyname)

    def query_datastates(self):
        for key, value in self.data.iteritems():
            if value:
                print("{} exists.".format(key))


class BasicInfo(object):
    def __init__(self):
        self.name = None
        self.layer = None
        self.space = None
        self.voxel_resolution = None

    def get_property(self):
        return self.name

    def set_property(self, name):
        self.name = name


class Geometry(BasicInfo):
    # Use anatomy for viz and analysis.
    def __init__(self):
        BasicInfo.__init__(self)

        self.coords = None
        self.faces = None
        pass

    def load_geometry(self, *args):
        io_operation(*args)
        self.coords = coords
        self.faces = faces
        pass

    def get_coords(self):
        if self.coords:
            return self.coords
        else:
            raise ValueError('Please load geometry first.')

    def get_faces(self):
        pass


class Morphology(BasicInfo):
    # Use anatomy for viz and analysis.
    def __init__(self):
        BasicInfo.__init__(self)

        self.curve = None
        self.thickness = None
        self.area = None
        pass

    def load_curve(self):
        io_operation(*args)
        self.curve = curve
        pass

    def get_curve(self):
        check_datastate('curve')
        return self.curve

    def load_thickness(self):
        io_operation(*args)
        self.thickness = thickness

    def get_thickness(self):
        check_datastate('thickness')
        return self.thickness


class Function(BasicInfo):
    # Load and operate functional data, like tvalue/zvalue from tfMRI, or timeseries from rsfMRI or movie-fMRI.
    def __init__(self):
        BasicInfo.__init__(self)

        self.tvalue = None
        self.timeseries = None
        pass

    def load_data(self, filepath):
        io_operation(filepath)
        # self.tvalue = tvalue
        self.timeseries = timeseries

    def get_data(self):
        return self.data

    def parcellation(self):
        MRFree.algorithm.function.parcellation(self.timeseries)


class Tract(object):
    pass


class Network(object):
    pass


class Gene(object):
    pass

