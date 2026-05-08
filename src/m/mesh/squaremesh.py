import numpy as np

from ElementConnectivity import ElementConnectivity
from mesh2d import mesh2d
from NodeConnectivity import NodeConnectivity


def squaremesh(md, Lx, Ly, nx, ny):
    """SQUAREMESH - create a structured square mesh

    This script will generate a structured square mesh
    Lx and Ly are the dimension of the domain (in meters)
    nx anx ny are the number of nodes in the x and y direction
    The coordinates x and y returned are in meters.

    Usage:
        [md] = squaremesh(md, Lx, Ly, nx, ny)
    """

    #get number of elements and number of nodes
    nel = (nx - 1) * (ny - 1) * 2
    nods = nx * ny

    #create coordinates
    n_grid, m_grid = np.meshgrid(np.arange(nx, dtype=np.float64),
                                 np.arange(ny, dtype=np.float64),
                                 indexing='ij')
    x = n_grid.ravel()
    y = m_grid.ravel()

    #create index — two triangles per cell, interleaved as
    # [A C B] at row 2m, [B C D] at row 2m+1, for each column n
    n_idx, m_idx = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1),
                               indexing='ij')
    A = n_idx * ny + (m_idx + 1)
    B = A + 1
    C = (n_idx + 1) * ny + (m_idx + 1)
    D = C + 1
    index = np.empty((nel, 3), dtype=int)
    index[0::2, :] = np.stack([A, C, B], axis=-1).reshape(-1, 3)
    index[1::2, :] = np.stack([B, C, D], axis=-1).reshape(-1, 3)

    #Scale  x and y
    x = x / np.max(x) * Lx
    y = y / np.max(y) * Ly

    #create segments
    segments = np.zeros((2 * (nx - 1) + 2 * (ny - 1), 3), int)
    #left edge:
    segments[0:ny - 1, :] = np.vstack((np.arange(2, ny + 1), np.arange(1, ny), (2 * np.arange(1, ny) - 1))).T
    #right edge:
    segments[ny - 1:2 * (ny - 1), :] = np.vstack((np.arange(ny * (nx - 1) + 1, nx * ny), np.arange(ny * (nx - 1) + 2, nx * ny + 1), 2 * np.arange((ny - 1) * (nx - 2) + 1, (nx - 1) * (ny - 1) + 1))).T
    #front edge:
    segments[2 * (ny - 1):2 * (ny - 1) + (nx - 1), :] = np.vstack((np.arange(2 * ny, ny * nx + 1, ny), np.arange(ny, ny * (nx - 1) + 1, ny), np.arange(2 * (ny - 1), 2 * (nx - 1) * (ny - 1) + 1, 2 * (ny - 1)))).T
    #back edge
    segments[2 * (ny - 1) + (nx - 1):2 * (nx - 1) + 2 * (ny - 1), :] = np.vstack((np.arange(1, (nx - 2) * ny + 2, ny), np.arange(ny + 1, ny * (nx - 1) + 2, ny), np.arange(1, 2 * (nx - 2) * (ny - 1) + 2, 2 * (ny - 1)))).T

    #plug coordinates and nodes
    md.mesh = mesh2d()
    md.mesh.x = x
    md.mesh.y = y
    md.mesh.numberofvertices = nods
    md.mesh.vertexonboundary = np.zeros(nods, int)
    md.mesh.vertexonboundary[segments[:, 0:2] - 1] = 1

    #plug elements
    md.mesh.elements = index
    md.mesh.segments = segments
    md.mesh.numberofelements = nel

    #Now, build the connectivity tables for this mesh.
    md.mesh.vertexconnectivity = NodeConnectivity(md.mesh.elements, md.mesh.numberofvertices)
    md.mesh.elementconnectivity = ElementConnectivity(md.mesh.elements, md.mesh.vertexconnectivity)

    return md
