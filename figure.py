import matplotlib.pyplot as plt


def figure(h=None):
    plt.figure(h)


def clf():
    plt.clf()
    plt.show(block=False)


def pause(seconds=0):
    try:
        plt.pause(seconds)
    except Exception:
        # can't invoke "update" command: application has been destroyed
        pass


def grid(enable):
    if isinstance(enable, str):
        enable = enable.lower()
        if enable in ["on", "true"]:
            enable = True
        if enable in ["off", "false"]:
            enable = False
    plt.grid(enable)
    plt.show(block=False)


def axis(opt):
    plt.axis(opt)
    plt.show(block=False)


def xlabel(name):
    plt.xlabel(name)
    plt.show(block=False)


def ylabel(name):
    plt.ylabel(name)
    plt.show(block=False)


def legend():
    try:
        plt.legend()
        plt.show(block=False)
    except:
        pass