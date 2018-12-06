import matplotlib.pyplot as plt


def figure(h=None):
    """
    Open a new figure or select an existing one.
    """
    plt.figure(h)


def close(h=None):
    """
    Close a figure.
    """
    plt.close(h)


def clf():
    """
    Clear the current figure.
    """
    plt.clf()
    plt.show(block=False)


def pause(seconds=0):
    """
    Stop the process.

    seconds         time to wait; if 0 (default) the user has to close
                    the current figure in order to continue.
    """
    try:
        plt.pause(seconds)
    except Exception:
        # can't invoke "update" command: application has been destroyed
        pass


def grid(enable):
    """
    Eanble/disable the grid on the current figure.

    enable      could be True, False, 0, 1, "true", "false", "on", "off" (case insensitive)
    """
    if isinstance(enable, str):
        enable = enable.lower()
        if enable in ["on", "true"]:
            enable = True
        if enable in ["off", "false"]:
            enable = False
    plt.grid(enable)
    plt.show(block=False)


def axis(opt):
    """
    Set the axes of the current figure.
    """
    plt.axis(opt)
    plt.show(block=False)


def xlabel(name):
    """
    Set the label of the X axis of the current figure.
    """
    plt.xlabel(name)
    plt.show(block=False)


def ylabel(name):
    """
    Set the label of the Y axis of the current figure.
    """
    plt.ylabel(name)
    plt.show(block=False)


def title(title):
    """
    Add a title to the current figure.
    """
    plt.title(title)
    plt.show(block=False)


def legend():
    """
    Show the legend according to the labels plots.
    """
    try:
        plt.legend()
        plt.show(block=False)
    except:
        pass