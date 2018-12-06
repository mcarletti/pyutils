import os
import glob
import torch
import torch.utils.data
import numpy as np
from .imageproc import imread


class Dataset(torch.utils.data.Dataset):
    """
    """


    def __init__(self, parent, mode, cbLoadSampleFun, cbPreprocessingFun=None):
        """
        Initialize the dataset.
        The file "root/dsname/mode.txt" will be loaded.
        It contains a list of pairs (filepath, target) where "filepath"
        is the path of the image file to load and "target" is the
        class index associated to that file.
        In the folder "root/dsname" there is also a "label.txt" file
        with the names of all the classes.

        parent              data folder containing the dataset
        mode                "data", "train", "valid" or "test"
        cbLoadSampleFun     function taking as parameter the filename of
                            the sample to load
        cbPreprocessingFun  function to preprocess the sample loaded
                            through "cbLoadSampleFun"
        """

        fpath = os.path.join(parent, mode + ".txt")
        data = np.loadtxt(fpath, dtype=str)

        self.filenames = [os.path.join(parent, x) for x in data[:,0]]
        self.targets = data[:,1].astype(np.int32)
        self.nSamples = len(self.filenames)
        self.nClasses = len(set(self.targets))
        self.cbLoadSampleFun = cbLoadSampleFun
        self.cbPreprocessingFun = cbPreprocessingFun


    def __getitem__(self, index):
        """
        Return a sample and its target values.

        index
        """

        x = self.cbLoadSampleFun(self.filenames[index])
        y = np.asarray(self.targets[index])

        if self.cbPreprocessingFun is not None:
            x, y = self.cbPreprocessingFun(x, y)
            
        return x, y


    def __len__(self):
        """
        Get the length of the dataset in terms of number of samples.
        """

        return self.nSamples
    

    def shuffle(self):
        """
        In place random permutation of the dataset.
        """

        idx = np.random.permutation(self.nSamples)
        self.filenames = np.asarray(self.filenames)[idx].tolist()
        self.targets = self.targets[idx]
