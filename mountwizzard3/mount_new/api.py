############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #  ####
#      ##  ##  #  ##  #     #
#     # # # #  # # # #     ###
#    #  ##  #  ##  ##        #
#   #   #   #  #   #     ####
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import logging
import PyQt5.QtCore
# external packages
# local imports
from mount_new.command import Command
from mount_new.configData import Data


class WorkerSignals(PyQt5.QtCore.QObject):
    """
    The WorkerSignals class offers a list of signals to be used and instantiated by the Worker
    class to get signals for error, finished and result to be transferred to the caller back
    """

    __all__ = ['WorkerSignals']
    version = '0.1'

    finished = PyQt5.QtCore.pyqtSignal()
    error = PyQt5.QtCore.pyqtSignal(object)
    result = PyQt5.QtCore.pyqtSignal(object)


class Worker(PyQt5.QtCore.QRunnable):
    """
    The Worker class offers a generic interface to allow any function to be executed as a thread
    in an threadpool
    """

    __all__ = ['Worker',
               'run']
    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        # the worker signal must not be a class variable, but instance otherwise
        # we get trouble when having multiple threads running
        self.signals = WorkerSignals()

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit(e)
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class Mount(object):
    """
    The Mount class is the main interface for interacting with the mount computer.
    The user could:
        setup / change the interface to the mount
        start / stop cyclic tasks to poll data from mount
        send and get data from mount
        has signals for interfacing to external GUI's for
            data updates, events, messages
    """

    __all__ = ['Mount',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self,
                 host=None,
                 pathToTimescaleData=None
                 ):

        # defining the data space for the mount
        self.data = Data(pathToTimescaleData=pathToTimescaleData)
        # defining the command interface to the mount
        self.command = Command(host=host,
                               data=self.data,
                               )
        self.threadpool = PyQt5.QtCore.QThreadPool()

