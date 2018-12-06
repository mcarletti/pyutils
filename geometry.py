import numpy as np


def norm(arr, axis=None):
    """
    Compute the norm of a vector.
    
    arr         input ndarray
    axis        axis along which norm is computed
    """

    return np.sqrt(np.sum(arr**2, axis=axis))


def lookAt(location, target, dtype=np.float32):
    """
    Compute the pose matrix (rotation, translation)
    of the camera which position is "location" and
    looks at "target" coordinates.
    X axis is parallel to the XY (world) plane
    Z axis points to "target".
    Y is the cross product of Z and X so that it point
    to the positive z-hemispace

    location        ndarray with 3 values
    target          ndarray with 3 values
    dtype           desired output data type (e.g. np.float32)
    """

    ZERO = 0.000001

    world_z = np.asarray([0, 0, 1])
    
    cam_z = target - location
    cam_z = cam_z / (norm(cam_z) + ZERO)
    
    cam_x = np.cross(world_z, cam_z)
    cam_x = cam_x / (norm(cam_x) + ZERO)
    
    cam_y = np.cross(cam_z, cam_x)
    cam_y = cam_y / (norm(cam_y) + ZERO)
    
    R = np.stack((cam_x, cam_y, cam_z)).T
    t = location

    posemtx = np.zeros((4,4))
    posemtx[0:3,0:3] = R
    posemtx[0:3, 3] = t
    posemtx[3,3] = 1

    return posemtx.astype(dtype)


def sampleSphere(nSamples=100):
    """
    Distributing many points on a sphere.
    SAFF, Edward B.; KUIJLAARS, Amo BJ.
    The mathematical intelligencer, 1997, 19.1: 5-11.

    nSamples        number of points on the unit spehere
    """
    s = 3.6 / np.sqrt(nSamples)
    dz = 2.0 / nSamples
    angle = 0.0
    z = 1 - dz / 2

    pts = np.zeros((nSamples, 3), dtype=np.float32)

    for i in range(nSamples):
        r = np.sqrt(1 - z * z)
        # compute coordinates
        x = np.cos(angle) * r
        y = np.sin(angle) * r
        pts[i] = [x, y, z]
        # update
        angle = angle + s / r
        z = z - dz
    
    return pts