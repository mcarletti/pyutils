import cv2
import scipy
import open3d
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def imread(filename, size=None, dtype=None, fmt=None):
    """
    Load an image file from disk.

    filename        path of the image file
    size            desired resolution as (W,H) tuple
    dtype           desired data type (e.g. np.float32)
    fmt             format of the image (e.g. "F" or "RGBA")
    """
    image = Image.open(filename)
    if size is not None and len(size) == 2:
        image = image.resize(size)
    if fmt is not None:
        image = image.convert(fmt)
    image = np.asarray(image)
    if dtype is not None:
        image = image.astype(dtype)
    return image


def imwrite(filename, image, fmt=None):
    """
    Save an image file from disk.

    filename        path of the image file
    image           ndarray to save as image
    fmt             format of the image (e.g. "F" or "RGBA")
    """
    src = Image.fromarray(image, fmt)
    src.save(filename)


def imresize(image, size):
    """
    Resize a ndarray.

    image           ndarray to resize
    size            desired resolution as (W,H) tuple
    """
    dst = cv2.resize(image, size)
    return dst

def imrotate(image, angle):
    """
    Rotate a ndarray.

    image           ndarray to resize
    angle           rotation angle in degrees
    """
    rows, cols = image.shape[:2]
    R = cv2.getRotationMatrix2D((rows//2, cols//2), angle, 1)
    dst = cv2.warpAffine(image, R, (rows, cols))
    return dst


def imblend(image1, image2, alpha=0.5):
    """
    Blend two images.

    image1          first ndarray
    image2          second ndarray
    alpha           normalized blending factor
    """
    if len(image1.shape) == 2:
        dst = alpha * image1 + (1. - alpha) * image2
    else:
        src1 = Image.fromarray(image1).convert("RGBA")
        src2 = Image.fromarray(image2).convert("RGBA")
        dst = Image.blend(src1, src2, alpha=alpha)
        dst = np.asarray(dst)
    return dst


def clf():
    plt.clf()


def pause(seconds=0):
    try:
        plt.pause(seconds)
    except Exception:
        # can't invoke "update" command: application has been destroyed
        pass


def imshow(image):
    """
    Show an image (non blocking).

    image           ndarray to visualize
    """
    plt.imshow(image)
    plt.show(block=False)


def imagesc(image):
    """
    Show an image after normalization (non blocking).

    image           ndarray to visualize
    """
    src = image.copy()
    dst = src - np.min(src)
    maxval = np.max(dst)
    if maxval > 0:
        dst = dst / maxval
    imshow(dst)


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
