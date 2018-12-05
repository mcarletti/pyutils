import os
import glob
import torch
import torch.utils.data
import numpy as np
from .imageproc import imread


class Dataset(torch.utils.data.Dataset):
    """
    """

    # def __init__(self, root, dsname, mode, cbPreprocessingFun=None):
    #     """
    #     Initialize the dataset.
    #     The "root/dsname" folder contains (at least) a folder named "mode".
    #     The "root/dsname/mode" folder contains a set of directories.
    #     Each folder is a class containing a set of images.
    #     The name of the folders are the labels of the classes, which indices
    #     are set according to the alphabetical order of the classes (e.g. if
    #     there are two classes "TRUCK" and "CAR", their id will be "1" and "0"
    #     respectively).
    #
    #     root        parent data folder
    #     dsname      name of the dataset
    #     mode        "train", "valid" or "test"
    #     """
    #
    #     searchpath = os.path.join(root, dsname, mode)
    #
    #     foldernames = [x.split("/")[-1] for x in glob.glob(os.path.join(searchpath, "*")) if os.path.isdir(x)]
    #     classnames = sorted(set(foldernames))
    #     self.nClasses = len(classnames)
    #
    #     if self.nClasses == 0:
    #         raise Exception("Number of classes is 0. Check search path")
    #
    #     labels = {}
    #     for i,x in enumerate(classnames):
    #         labels[x] = i
    #
    #     self.filenames = sorted(glob.glob(os.path.join(searchpath, "*/*.jpg")))
    #     self.nSamples = len(self.filenames)
    #
    #     self.targets = [-1] * self.nSamples
    #     for i,x in enumerate(self.filenames):
    #         cname = x.split("/")[-2]
    #         self.targets[i] = labels[cname]
    #
    #     self.cbPreprocessingFun = cbPreprocessingFun


    def __init__(self, parent, mode, cbLoadImageFun=None, cbPreprocessingFun=None):
        """
        Initialize the dataset.
        The file "root/dsname/mode.txt" will be loaded.
        It contains a list of pairs (filepath, target) where "filepath"
        is the path of the image file to load and "target" is the
        class index associated to that file.
        In the folder "root/dsname" there is also a "label.txt" file
        with the names of all the classes.

        parent      data folder containing the dataset
        mode        "train", "valid" or "test"
        """

        fpath = os.path.join(parent, mode + ".txt")
        data = np.loadtxt(fpath, dtype=str)

        self.filenames = [os.path.join(parent, x) for x in data[:,0]]
        self.targets = data[:,1].astype(np.int32)
        self.nSamples = len(self.filenames)
        self.nClasses = len(set(self.targets))
        self.cbLoadImageFun = cbLoadImageFun
        self.cbPreprocessingFun = cbPreprocessingFun


    def __getitem__(self, index):
        """
        Return a sample and its index.
        """

        if self.cbLoadImageFun is None:
            x = imread(self.filenames[index], dtype=np.uint8, fmt="RGB")
        else:
            x = self.cbLoadImageFun(self.filenames[index])
            
        y = np.asarray(self.targets[index])

        if self.cbPreprocessingFun is not None:
            x, y = self.cbPreprocessingFun(x, y)
            
        return x, y


    def __len__(self):
        """
        Get the length of the dataset in term of number of samples.
        """

        return self.nSamples
    

    def shuffle(self):
        """
        Random permutation of the dataset.
        """

        idx = np.random.permutation(self.nSamples)
        self.filenames = np.asarray(self.filenames)[idx].tolist()
        self.targets = self.targets[idx]
