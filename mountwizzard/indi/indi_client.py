############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
import logging
import time
import threading
from xml.etree import ElementTree
import PyQt5
from PyQt5 import QtCore, QtNetwork, QtWidgets
import indi.indi_xml as indiXML
import astropy.io.fits as pyfits
from baseclasses import checkParamIP


class INDIClient(PyQt5.QtCore.QObject):
    finished = PyQt5.QtCore.pyqtSignal()
    logger = logging.getLogger(__name__)
    received = QtCore.pyqtSignal(object)
    status = QtCore.pyqtSignal(int)

    GENERAL_INTERFACE = 0
    TELESCOPE_INTERFACE = (1 << 0)
    CCD_INTERFACE = (1 << 1)
    GUIDER_INTERFACE = (1 << 2)
    FOCUSER_INTERFACE = (1 << 3)
    FILTER_INTERFACE = (1 << 4)
    DOME_INTERFACE = (1 << 5)
    GPS_INTERFACE = (1 << 6)
    WEATHER_INTERFACE = (1 << 7)
    AO_INTERFACE = (1 << 8)
    DUSTCAP_INTERFACE = (1 << 9)
    LIGHTBOX_INTERFACE = (1 << 10)
    DETECTOR_INTERFACE = (1 << 11)
    AUX_INTERFACE = (1 << 15)

    data = {
        'ServerIP': '',
        'ServerPort': 7624,
        'Connected': False,
        'DriverNameCCD': '',
        'DriverNameFilter': '',
        'DriverNameTelescope': '',
        'DriverNameWeather': '',
        'Device': {}
    }

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.isRunning = False
        self.ipChangeLock = threading.Lock()
        self._mutex = PyQt5.QtCore.QMutex()
        self.checkIP = checkParamIP.CheckIP()
        self.socket = None
        self.settingsChanged = False
        self.receivedImage = False
        self.imagePath = ''
        self.messageString = ''

    def initConfig(self):
        try:
            if 'INDIServerPort' in self.app.config:
                self.app.ui.le_INDIServerPort.setText(self.app.config['INDIServerPort'])
            if 'INDIServerIP' in self.app.config:
                self.app.ui.le_INDIServerIP.setText(self.app.config['INDIServerIP'])
            if 'CheckEnableINDI' in self.app.config:
                self.app.ui.checkEnableINDI.setChecked(self.app.config['CheckEnableINDI'])
        except Exception as e:
            self.logger.error('item in config.cfg not be initialize, error:{0}'.format(e))
        finally:
            pass
        self.setIP()
        self.setPort()
        # have to choose lambda to get the right threading context
        self.app.ui.checkEnableINDI.stateChanged.connect(lambda: self.enableDisableINDI())
        # setting changes in gui on false, because the set of the config changed them already
        self.settingsChanged = False
        self.app.ui.le_INDIServerIP.textChanged.connect(self.setIP)
        self.app.ui.le_INDIServerIP.editingFinished.connect(self.changedINDIClientConnectionSettings)
        self.app.ui.le_INDIServerPort.textChanged.connect(self.setPort)
        self.app.ui.le_INDIServerPort.editingFinished.connect(self.changedINDIClientConnectionSettings)

    def storeConfig(self):
        self.app.config['INDIServerPort'] = self.app.ui.le_INDIServerPort.text()
        self.app.config['INDIServerIP'] = self.app.ui.le_INDIServerIP.text()
        self.app.config['CheckEnableINDI'] = self.app.ui.checkEnableINDI.isChecked()

    def changedINDIClientConnectionSettings(self):
        print('indi restart')
        if self.settingsChanged:
            print('changed')
            self.settingsChanged = False
            self.app.messageQueue.put('Setting IP address/port for INDI client: {0}:{1}\n'.format(self.data['ServerIP'], self.data['ServerPort']))
            if self.app.ui.checkEnableINDI.isChecked():
                self.ipChangeLock.acquire()
                self.stop()
                time.sleep(1)
                self.app.threadINDI.start()
                self.ipChangeLock.release()

    def setPort(self):
        valid, value = self.checkIP.checkPort(self.app.ui.le_INDIServerPort)
        self.settingsChanged = (self.data['ServerPort'] != value)
        if valid:
            self.data['ServerPort'] = value

    def setIP(self):
        valid, value = self.checkIP.checkIP(self.app.ui.le_INDIServerIP)
        self.settingsChanged = (self.data['ServerIP'] != value)
        if valid:
            self.data['ServerIP'] = value

    def enableDisableINDI(self):
        print('check')
        if self.app.ui.checkEnableINDI.isChecked():
            if not self.isRunning:
                self.app.threadINDI.start()
        else:
            if self.isRunning:
                self.stop()

    def run(self):
        if not self.isRunning:
            self.isRunning = True
        self.socket = QtNetwork.QTcpSocket()
        self.socket.hostFound.connect(self.handleHostFound)
        self.socket.connected.connect(self.handleConnected)
        self.socket.stateChanged.connect(self.handleStateChanged)
        self.socket.disconnected.connect(self.handleDisconnect)
        self.socket.error.connect(self.handleError)
        self.socket.readyRead.connect(self.handleReadyRead)
        self.socket.connectToHost(self.data['ServerIP'], self.data['ServerPort'])
        self.received.connect(self.handleReceived)
        while self.isRunning:
            time.sleep(0.2)
            if not self.app.INDICommandQueue.empty():
                indi_command = self.app.INDICommandQueue.get()
                self.sendMessage(indi_command)
            QtWidgets.QApplication.processEvents()
            if not self.data['Connected'] and self.socket.state() == 0:
                self.socket.readyRead.connect(self.handleReadyRead)
                self.socket.connectToHost(self.data['ServerIP'], self.data['ServerPort'])
        # if I leave the loop, I close the connection to remote host
        self.socket.disconnectFromHost()

    def stop(self):
        self._mutex.lock()
        self.isRunning = False
        self._mutex.unlock()
        self.finished.emit()

    def handleHostFound(self):
        pass

    def handleConnected(self):
        self.data['Connected'] = True
        self.logger.info('INDI Server connected at {0}:{1}'.format(self.data['ServerIP'], self.data['ServerPort']))
        self.app.INDICommandQueue.put(indiXML.clientGetProperties(indi_attr={'version': '1.0'}))

    def handleError(self, socketError):
        self.logger.error('INDI connection fault: {0}, error: {1}'.format(self.socket.errorString(), socketError))

    def handleStateChanged(self):
        self.status.emit(self.socket.state())

    def handleDisconnect(self):
        self.logger.info('INDI client connection is disconnected from host')
        self.data['DriverNameCCD'] = ''
        self.data['DriverNameFilter'] = ''
        self.data['DriverNameTelescope'] = ''
        self.data['DriverNameWeather'] = ''
        self.data['Connected'] = False
        self.app.INDIStatusQueue.put({'Name': 'Weather', 'value': '---'})
        self.app.INDIStatusQueue.put({'Name': 'CCD', 'value': '---'})
        self.app.INDIStatusQueue.put({'Name': 'Telescope', 'value': '---'})
        self.app.INDIStatusQueue.put({'Name': 'Filter', 'value': '---'})

    def handleReceived(self, message):
        # central dispatcher for data coming from INDI devices. I makes the whole status and data evaluation and fits the
        # data to mountwizzard
        if isinstance(message, indiXML.SetBLOBVector) or isinstance(message, indiXML.DefBLOBVector):
            device = message.attr['device']
            if device == self.data['DriverNameCCD']:
                name = message.attr['name']
                if name == 'CCD1':
                    if 'format' in message.getElt(0).attr:
                        if message.getElt(0).attr['format'] == '.fits':
                            imageHDU = pyfits.HDUList.fromstring(message.getElt(0).getValue())
                            imageHDU.writeto(self.imagePath)
                            self.logger.info('image file is in raw fits format')
                        else:
                            self.logger.info('image file is not in raw fits format')
                        self.receivedImage = True

        elif isinstance(message, indiXML.DelProperty):
            device = message.attr['device']
            if device in self.data['Device']:
                if 'name' in message.attr:
                    group = message.attr['name']
                    if group in self.device[device]:
                        del self.data['Device'][device][group]
        else:
            device = message.attr['device']
            if device not in self.data['Device']:
                self.data['Device'][device] = {}
            if 'name' in message.attr:
                group = message.attr['name']
                if group not in self.data['Device'][device]:
                    self.data['Device'][device][group] = {}
                for elt in message.elt_list:
                    self.data['Device'][device][group][elt.attr['name']] = elt.getValue()

        if 'name' in message.attr:
            if message.attr['name'] == 'DRIVER_INFO':
                if message.elt_list[3].attr['name'] == 'DRIVER_INTERFACE':
                    if int(message.getElt(3).getValue()) & self.TELESCOPE_INTERFACE:
                        self.data['DriverNameTelescope'] = message.getElt(0).getValue()
                        self.app.INDIStatusQueue.put({'Name': 'Telescope', 'value': message.getElt(0).getValue()})
                    elif int(message.getElt(3).getValue()) & self.CCD_INTERFACE:
                        self.data['DriverNameCCD'] = message.getElt(0).getValue()
                        self.app.INDIStatusQueue.put({'Name': 'CCD', 'value': message.getElt(0).getValue()})
                    elif int(message.getElt(3).getValue()) & self.FILTER_INTERFACE:
                        self.data['DriverNameFilter'] = message.getElt(0).getValue()
                        self.app.INDIStatusQueue.put({'Name': 'Filter', 'value': message.getElt(0).getValue()})
                    elif int(message.getElt(3).getValue()) == self.WEATHER_INTERFACE:
                        self.data['DriverNameWeather'] = message.getElt(0).getValue()
                        self.app.INDIStatusQueue.put({'Name': 'Weather', 'value': message.getElt(0).getValue()})

    def handleReadyRead(self):
        # Add starting tag if this is new message.
        if len(self.messageString) == 0:
            self.messageString = "<data>"

        # Get message from socket.
        while self.socket.bytesAvailable():
            # print(self.socket.bytesAvailable())
            tmp = str(self.socket.read(1000000), "ascii")
            self.messageString += tmp

        # Add closing tag.
        self.messageString += "</data>"

        # Try and parse the message.
        try:
            messages = ElementTree.fromstring(self.messageString)
            self.messageString = ""
            for message in messages:
                xml_message = indiXML.parseETree(message)
                self.handleReceived(xml_message)

        # Message is incomplete, remove </data> and wait..
        except ElementTree.ParseError:
            self.messageString = self.messageString[:-7]

    def sendMessage(self, indi_command):
        if self.socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            self.socket.write(indi_command.toXML() + b'\n')
            self.socket.flush()
        else:
            self.logger.warning('Socket not connected')
