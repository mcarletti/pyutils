import open3d
import numpy as np
import matplotlib.pyplot as plt


def plot(X, Y=None, clr="b", label=""):
    """
    2D plot using matplotlib.

    X               first dimension; if Y is None, shape of X must be Nx1 or Nx2
    Y               second dimension
    """

    if Y is None:
        if len(X.shape) == 1:
            xx = np.arange(X.size)
            yy = X
        if len(X.shape) == 2:
            xx = X[:,0]
            yy = X[:,1]
    else:
        xx = X
        yy = Y

    plt.plot(xx, yy, clr, label=label)
    plt.show(block=False)


def plot3(X, Y=None, Z=None, clr="b", xlabel=None, ylabel=None, zlabel=None):
    """
    3D plot using matplotlib.

    X               first dimension; if Y and Z are None, shape of X must be Nx3
    Y               second dimension
    Z               third dimension
    """

    # TODO
    pass


def scatter(X, Y=None):
    """
    2D scatter plot using matplotlib.

    X               first dimension; if Y is None, shape of X must be Nx2
    Y               second dimension
    """
    if Y is None:
        xy = X
    else:
        xy = np.stack((X,Y),axis=-1)
    plt.scatter(xy[:,0], xy[:,1])
    plt.show(block=False)


def scatter3(X, Y=None, Z=None):
    """
    3D scatter plot using Open3D lib.

    X               first dimension; if Y and Z are None, shape of X must be Nx3
    Y               second dimension
    Z               third dimension
    """
    if Y is None and Z is None:
        xyz = X
    else:
        xyz = np.stack((X,Y,Z),axis=-1)
    pcd = open3d.PointCloud()
    pcd.points = open3d.Vector3dVector(xyz)
    open3d.draw_geometries([pcd])