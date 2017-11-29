############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017
#
# Licence APL2.0
#
############################################################
import logging
# import PyQT5 for threading purpose
import PyQt5
from mount import ipdirect
from astrometry import transform


class MountStatusRunner(PyQt5.QtCore.QObject):
    logger = logging.getLogger(__name__)
    finished = PyQt5.QtCore.pyqtSignal()

    signalStatusCamera = PyQt5.QtCore.pyqtSignal(int)
    signalStatusSolver = PyQt5.QtCore.pyqtSignal(int)
    signalModelPointsRedraw = PyQt5.QtCore.pyqtSignal(bool)

    BLUE = 'background-color: rgb(42, 130, 218)'
    RED = 'background-color: red;'
    DEFAULT = 'background-color: rgb(32,32,32); color: rgb(192,192,192)'

    CYCLESTATUSSLOW = 10000
    CYCLESTATUSMEDIUM = 3000
    CYCLESTATUSFAST = 200

    def __init__(self, parent, app):
        super().__init__()
        self.isRunning = False
        self._mutex = PyQt5.QtCore.QMutex()
        # make main sources available
        self.app = app
        self.parent = parent
        self.transform = transform.Transform(self.app)
        self.mountIpDirect = ipdirect.MountIpDirect(self.app)

    def initConfig(self):
        self.mountIpDirect.initConfig()
        self.mountIpDirect.mountPort = 3490

    def storeConfig(self):
        pass

    def run(self):
        if not self.isRunning:
            self.isRunning = True
        self.mountIpDirect.connect()
        self.getStatusOnce()
        self.getStatusFast()
        self.getStatusMedium()
        self.getStatusSlow()

    def stop(self):
        self.mountIpDirect.disconnect()
        self._mutex.lock()
        self.isRunning = False
        self._mutex.unlock()
        self.finished.emit()

    def setRefractionParam(self):
        if 'Temperature' in self.app.workerAscomEnvironment.data and 'Pressure' in self.app.workerAscomEnvironment.data and self.app.workerAscomEnvironment.isRunning:
            pressure = self.app.workerAscomEnvironment.data['Pressure']
            temperature = self.app.workerAscomEnvironment.data['Temperature']
            if (900.0 < pressure < 1100.0) and (-40.0 < temperature < 50.0):
                self.mountIpDirect.sendCommand('SRPRS{0:04.1f}'.format(pressure))
                if temperature > 0:
                    self.mountIpDirect.sendCommand('SRTMP+{0:03.1f}'.format(temperature))
                else:
                    self.mountIpDirect.sendCommand('SRTMP-{0:3.1f}'.format(-temperature))
                self.parent.data['RefractionTemperature'] = self.mountIpDirect.sendCommand('GRTMP')
                self.parent.data['RefractionPressure'] = self.mountIpDirect.sendCommand('GRPRS')
            else:
                self.logger.warning('parameters out of range ! temperature:{0} pressure:{1}'.format(temperature, pressure))

    def getStatusFast(self):
        print('Fast')
        reply = self.mountIpDirect.sendCommand('GS')
        if len(reply) > 0:
            self.parent.data['LocalSiderealTime'] = reply.strip('#')
        # reply = self.mountIpDirect.sendCommand('GR')
        # if len(reply) > 0:
        #     self.parent.data['RaJNow'] = self.transform.degStringToDecimal(reply)
        # reply = self.mountIpDirect.sendCommand('GD')
        # if len(reply) > 0:
        #     self.parent.data['DecJNow'] = self.transform.degStringToDecimal(reply)
        reply = self.mountIpDirect.sendCommand('Ginfo')
        if len(reply) > 0:
            try:
                reply = reply.rstrip('#').strip().split(',')
            except Exception as e:
                self.logger.error('receive error Ginfo command: {0} reply:{1}'.format(e, reply))
            finally:
                pass
            if len(reply) == 8:
                self.parent.data['RaJNow'] = float(reply[0])
                self.parent.data['DecJNow'] = float(reply[1])
                self.parent.data['Pierside'] = reply[2]
                self.parent.data['Az'] = float(reply[3])
                self.parent.data['Alt'] = float(reply[4])
                # needed for 2.14. firmware
                self.parent.data['JulianDate'] = reply[5].rstrip('#')
                self.parent.data['Status'] = int(reply[6])
                self.parent.data['Slewing'] = (reply[7] == '1')

                self.parent.data['RaJ2000'], self.parent.data['DecJ2000'] = self.transform.transformERFA(self.parent.data['RaJNow'], self.parent.data['DecJNow'], 2)
                self.parent.data['TelescopeRA'] = '{0}'.format(self.transform.decimalToDegree(self.parent.data['RaJ2000'], False, False))
                self.parent.data['TelescopeDEC'] = '{0}'.format(self.transform.decimalToDegree(self.parent.data['DecJ2000'], True, False))
                self.parent.data['TelescopeAltitude'] = '{0:03.2f}'.format(self.parent.data['Alt'])
                self.parent.data['TelescopeAzimuth'] = '{0:03.2f}'.format(self.parent.data['Az'])
                self.parent.data['MountStatus'] = '{0}'.format(self.parent.data['Status'])
                self.parent.data['JulianDate'] = '{0}'.format(self.parent.data['JulianDate'][:13])
                if self.parent.data['Pierside'] == str('W'):
                    self.parent.data['TelescopePierSide'] = 'WEST'
                else:
                    self.parent.data['TelescopePierSide'] = 'EAST'
                self.parent.signalMountAzAltPointer.emit(self.parent.data['Az'], self.parent.data['Alt'])
            else:
                self.logger.warning('Ginfo command delivered wrong number of arguments: {0}'.format(reply))
        if self.isRunning:
            PyQt5.QtCore.QTimer.singleShot(self.CYCLESTATUSFAST, self.getStatusFast)
            PyQt5.QtWidgets.QApplication.processEvents()

    def getStatusMedium(self):
        print('Medium')
        if self.app.ui.checkAutoRefractionNotTracking.isChecked():
            # if there is no tracking, than updating is good
            if 'Status' in self.parent.data:
                if self.parent.data['Status'] != 0:
                    self.setRefractionParam()
        if self.app.ui.checkAutoRefractionCamera.isChecked():
            # the same is good if the camera is not in integrating
            if self.app.workerModelingDispatcher.modelingRunner.imagingApps.imagingWorkerAppHandler.data['CameraStatus'] in ['READY - IDLE', 'DOWNLOADING']:
                self.setRefractionParam()
        self.parent.data['SlewRate'] = self.mountIpDirect.sendCommand('GMs')
        self.parent.data['TimeToFlip'] = int(float(self.mountIpDirect.sendCommand('Gmte')))
        self.parent.data['MeridianLimitTrack'] = int(float(self.mountIpDirect.sendCommand('Glmt')))
        self.parent.data['MeridianLimitSlew'] = int(float(self.mountIpDirect.sendCommand('Glms')))
        self.parent.data['TimeToMeridian'] = int(self.parent.data['TimeToFlip'] - self.parent.data['MeridianLimitTrack'] / 360 * 24 * 60)

        self.parent.signalMountTrackPreview.emit()
        if self.isRunning:
            PyQt5.QtCore.QTimer.singleShot(self.CYCLESTATUSMEDIUM, self.getStatusMedium)
            PyQt5.QtWidgets.QApplication.processEvents()

    def getStatusSlow(self):
        print('Slow')
        self.parent.data['TimeToTrackingLimit'] = self.mountIpDirect.sendCommand('Gmte')
        self.parent.data['RefractionTemperature'] = self.mountIpDirect.sendCommand('GRTMP')
        self.parent.data['RefractionPressure'] = self.mountIpDirect.sendCommand('GRPRS')
        self.parent.data['TelescopeTempDEC'] = self.mountIpDirect.sendCommand('GTMP1')
        self.parent.data['RefractionStatus'] = self.mountIpDirect.sendCommand('GREF')
        self.parent.data['UnattendedFlip'] = self.mountIpDirect.sendCommand('Guaf')
        self.parent.data['MeridianLimitTrack'] = self.mountIpDirect.sendCommand('Glmt')
        self.parent.data['MeridianLimitSlew'] = self.mountIpDirect.sendCommand('Glms')
        self.parent.data['DualAxisTracking'] = self.mountIpDirect.sendCommand('Gdat')
        self.parent.data['CurrentHorizonLimitHigh'] = self.mountIpDirect.sendCommand('Gh')
        self.parent.data['CurrentHorizonLimitLow'] = self.mountIpDirect.sendCommand('Go')
        try:
            if self.parent.data['FW'] < 21500:
                return
            reply = self.mountIpDirect.sendCommand('GDUTV')
            if len(reply) > 0:
                valid, expirationDate = reply.split(',')
                self.parent.data['UTCDataValid'] = valid
                self.parent.data['UTCDataExpirationDate'] = expirationDate
        except Exception as e:
            self.logger.error('receive error GDUTV command: {0}'.format(e))
        finally:
            pass
        if self.isRunning:
            PyQt5.QtCore.QTimer.singleShot(self.CYCLESTATUSSLOW, self.getStatusSlow)
            PyQt5.QtWidgets.QApplication.processEvents()

    def getStatusOnce(self):
        # Set high precision mode
        self.mountIpDirect.sendCommand('U2')
        self.parent.site_height = self.mountIpDirect.sendCommand('Gev')
        lon1 = self.mountIpDirect.sendCommand('Gg')
        # due to compatibility to LX200 protocol east is negative
        if lon1[0] == '-':
            self.parent.site_lon = lon1.replace('-', '+')
        else:
            self.parent.site_lon = lon1.replace('+', '-')
        self.parent.site_lat = self.mountIpDirect.sendCommand('Gt')
        self.parent.data['CurrentSiteElevation'] = self.parent.site_height
        self.parent.data['CurrentSiteLongitude'] = lon1
        self.parent.data['CurrentSiteLatitude'] = self.parent.site_lat
        self.parent.data['FirmwareDate'] = self.mountIpDirect.sendCommand('GVD')
        self.parent.data['FirmwareNumber'] = self.mountIpDirect.sendCommand('GVN')
        fw = self.parent.data['FirmwareNumber'].split('.')
        if len(fw) == 3:
            self.parent.data['FW'] = int(float(fw[0]) * 10000 + float(fw[1]) * 100 + float(fw[2]))
        else:
            self.parent.data['FW'] = 0
        self.parent.data['FirmwareProductName'] = self.mountIpDirect.sendCommand('GVP')
        self.parent.data['FirmwareTime'] = self.mountIpDirect.sendCommand('GVT')
        self.parent.data['HardwareVersion'] = self.mountIpDirect.sendCommand('GVZ')
        self.logger.info('FW: {0} Number: {1}'.format(self.mountIpDirect.sendCommand('GVN'), self.parent.data['FW']))
        self.logger.info('Site Lon:{0}'.format(self.parent.site_lon))
        self.logger.info('Site Lat:{0}'.format(self.parent.site_lat))
        self.logger.info('Site Height:{0}'.format(self.parent.site_height))
