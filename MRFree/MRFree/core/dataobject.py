import numpy as np
import nibabel as nib


class Region(object):
    def __init__(self, name, mask=1):
        self.name = name
        self.mask = mask
        self.scalar = {}
        self.coords = None
        self.faces = None

    def load_geometry(self, source):
        coords, faces = nib.freesurfer.io.read_geometry(source)
        self.coords = getregioncoords(coords, mask)
        self.faces = getregionfaces(faces, mask)
        pass

    def load_scalar(self, source, key):
        data = nib.load(source)
        if not self.scalar.has_key(key):
            self.scalar[key] = applymask(data, self.mask)
        else:
            self.scalar[key] = np.append(self.scalar[key], data, axis=0)

    def get_coords(self):
        return self.coords

    def set_coords(self, coords):
        self.coords = coords

    def get_faces(self):
        return self.faces

    def set_faces(self, faces):
        self.faces = faces

    def get_scalar(self, datatype):
        return self.scalar[datatype]

    def set_scalar(self, datatype, data):
        self.scalar[datatype] = data

    def merge(self, data):


class SurfRegion(Region):
    def load_geometry(self):
        pass

    def load_scalar(self):
        pass


class VolRegion(Region):
    pass


def applymask(data, mask):
    if situation1:
        return data * mask
    if situation2:
        zeros = np.where(mask == 0)
        return np.delete(data, zeros, axis=0)
    raise ValueError("Wrong situation.")
