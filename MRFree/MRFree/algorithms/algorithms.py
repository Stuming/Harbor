from sklearn.cluster.spectral import SpectralClustering


# In algorithm
def operation(data1, data2):
    pass


def add(data1, data2):
    data1, data2 = check_shape(data1, data2)
    return data1 + data2


def apply_mask(data, mask):
    data, mask = check_shape(data, mask)
    return data * mask


def check_shape(data1, data2):
    if not np.shape(data1) == np.shape(data2):
        data2 = np.reshape(data2, np.shape(data1))
    return data1, data2


def parcellation(*args):
    sklearn.cluster(*args)
