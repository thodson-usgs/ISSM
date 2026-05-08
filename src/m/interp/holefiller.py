import numpy as np
from scipy.spatial import cKDTree


def nearestneighbors(x, y, data, goodids, badids, knn):
    '''
    fill holes using nearest neigbors.  Arguments include:


    x, y:        the coordinates of data to be filled
    data:        the data field to be filled (full field, including holes)
    goodids:    id's into the vertices that have good data
    badids:    id's into the vertices with missing / bad data
    knn:        integer representing the k nearest neighbors to use for filling
                holes.  The average data value over the k nearest neighbors is
                then used to fill the hole.

    Usage:
        filleddata = nearestneighbors(x, y, data, goodids, badids, knn)

    Example:
        filledthickness = nearestneighbors(x, y, data, goodids, badids, 5)
    '''

    if type(knn) != int or knn < 1:
        raise TypeError('nearestneighbors error: knn should be an integer > 1')

    if len(x) != len(data) or len(y) != len(data):
        raise Exception('nearestneighbors error: x and y should have the same length as "data"')

    filled = data

    XYGood = np.dstack([x[goodids], y[goodids]])[0]
    XYBad = np.dstack([x[badids], y[badids]])[0]
    tree = cKDTree(XYGood)
    nearest = tree.query(XYBad, k=knn)[1]

    goodvals = filled[goodids]
    if knn == 1:
        filled[badids] = goodvals[nearest]
    else:
        filled[badids] = goodvals[nearest].mean(axis=1)

    return filled
