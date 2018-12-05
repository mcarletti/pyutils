# Python Utils

Set of utility functions to (mainly) load, save and visualize data.

The API is intended to be similar to the MATLAB interface, in particular for image processing and plot/scatter functions.

Visualization functions (i.e. plot, scatter) use matplotlib for 2D and Open3D for 3D.

Serialization supported formats:
* TXT (using numpy loadtxt and savetxt functions)
* YAML
* INIT/CFG (`TODO`)
* NPY
* NPZ (contains one file called *data*)
* MAT (based on scipy.io package)


