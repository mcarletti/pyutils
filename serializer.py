import yaml
import numpy as np
import scipy.io as sio


def load(filename):
    """
    Load file.
    Supported formats:
        TXT
        YAML
        MAT
        NPY
        NPZ
    """

    ext = filename.split(".")[-1]

    if ext in ["txt"]:
        data = np.loadtxt(filename)

    if ext in ["yml", "yaml"]:
        with open(filename, "r") as fp:
            data = yaml.load(fp)

    if ext in ["mat"]:
        data = sio.loadmat(filename)
        for k in data.keys():
            data[k] = np.squeeze(data[k])

    if ext in ["npy", "npz"]:
        data = np.load(filename)
        data = data.any()
    
    return data


def save(filename, data):
    """
    Save data into a file.
    Supported formats:
        TXT
        YAML
        MAT
        NPY
        NPZ
    
    data            values to store formatted according
                    to the desired output file format
    """

    ext = filename.split(".")[-1]

    if ext in ["txt"]:
        np.savetxt(filename, data, fmt="%s")

    if ext in ["yml", "yaml"]:
        with open(filename, "w") as fp:
            yaml.dump(data)

    if ext in ["mat"]:
        sio.savemat(filename, data, do_compression=True)

    if ext in ["npy"]:
        np.save(filename, data)

    if ext in ["npz"]:
        np.savez(filename, data)
