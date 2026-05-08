import numpy as np


def GetAreas3DTria(index, x, y, z, *args):
    """GETAREAS3DTRIA - compute areas of triangles with 3D coordinates

    Compute areas of triangles with 3D coordinates.

    Usage:
        areas = GetAreas3DTria(index, x, y, z)

    Examples:
        areas = GetAreas3DTria(md.mesh.elements, md.mesh.x, md.mesh.y, md.mesh.z)

    TODO:
    - Determine if *args is needed.
    """

    nods = len(x)

    # Some checks
    nargs = len(args)

    # TODO: Do we really need this under Python (first 4 arguments are required)?
    # if nargs != 3 and nargs != 4:
    #     print(GetAreas3DTria.__doc__)
    #     raise Exception('GetAreas3DTria error message: bad usage')

    if len(y) != nods or (nargs == 4 and len(z) != nods):
        print(GetAreas3DTria.__doc__)
        raise Exception('GetAreas3DTria error message: x, y, and z do not have the same length')

    if np.max(index) > nods:
        print(GetAreas3DTria.__doc__)
        raise Exception('GetAreas3DTria error message: index should not have values above {}'.format(nods))

    if nargs == 4 and index.shape[1] != 3:
        print(GetAreas3DTria.__doc__)
        raise Exception('GetAreas3DTria error message: index should have 3 columns for 2d meshes')

    # Vertex coordinates per triangle (1-based ids -> 0-based indices)
    p1 = np.column_stack((x[index[:, 0] - 1], y[index[:, 0] - 1], z[index[:, 0] - 1]))
    p2 = np.column_stack((x[index[:, 1] - 1], y[index[:, 1] - 1], z[index[:, 1] - 1]))
    p3 = np.column_stack((x[index[:, 2] - 1], y[index[:, 2] - 1], z[index[:, 2] - 1]))

    # Area = 0.5 * |edge1 × edge2|
    return 0.5 * np.linalg.norm(np.cross(p2 - p1, p3 - p1), axis=1)
