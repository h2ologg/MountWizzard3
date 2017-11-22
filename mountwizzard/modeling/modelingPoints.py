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
import os
import copy
from astrometry import transform
# for the sorting
import operator


class ModelPoints:
    logger = logging.getLogger(__name__)

    def __init__(self, app):
        self.app = app
        self.transform = transform.Transform(app)
        self.horizonPoints = []
        self.BasePoints = []
        self.RefinementPoints = []

    def loadModelPoints(self, modelPointsFileName, modeltype):
        p = []
        number = 0
        msg = None
        if modelPointsFileName.strip() == '':
            msg = 'No Model Points Filename given!'
            self.logger.warning('No Model Points Filename given!')
            return p, msg
        try:
            with open('config/' + modelPointsFileName, 'r') as fileHandle:
                for line in fileHandle:
                    if line.startswith('GRID'):
                        # if grid, then its a TSX file (the sky x)
                        convertedLine = line.rstrip('\n').split()
                        point = (float(convertedLine[2]), float(convertedLine[3]))
                        number += 1
                        if modeltype == 'Refinement' and number > 3:
                            p.append(point)
                        elif modeltype == 'Base' and number <= 3:
                            p.append(point)
                    else:
                        # format is same as Per's Model Maker
                        convertedLine = line.rstrip('\n').split(':')
                        point = (int(convertedLine[0]), int(convertedLine[1]))
                        if len(convertedLine) == 2 and modeltype == 'Refinement':
                            p.append(point)
                        elif len(convertedLine) != 2 and modeltype == 'Base':
                            p.append(point)
        except Exception as e:
            msg = 'Error loading modeling points from file [{0}] error: {1}!'.format(modelPointsFileName, e)
            self.logger.warning('Error loading modeling points from file [{0}] error: {1}!'.format(modelPointsFileName, e))
        finally:
            return p, msg

    def sortPoints(self, modeltype):
        if modeltype == 'Base':
            points = self.BasePoints
        else:
            points = self.RefinementPoints
        if len(points) == 0:
            self.logger.warning('There are no {0}points to sort'.format(modeltype))
            return
        westSide = []
        eastSide = []
        a = sorted(points, key=operator.itemgetter(0))
        for i in range(0, len(a)):
            if a[i][0] >= 180:
                westSide.append((a[i][0], a[i][1]))
            else:
                eastSide.append((a[i][0], a[i][1]))
        westSide = sorted(westSide, key=operator.itemgetter(1))
        eastSide = sorted(eastSide, key=operator.itemgetter(1))
        if modeltype == 'Base':
            self.BasePoints = eastSide + westSide
        else:
            self.RefinementPoints = eastSide + westSide
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def loadHorizonPoints(self, horizonPointsFileName, file_check, line_check, line_value):
        self.horizonPoints = []
        hp = []
        msg = None
        minAlt = 0
        if file_check:
            if horizonPointsFileName == '':
                msg = 'No horizon points filename given !'
                return msg
            if not os.path.isfile(os.getcwd() + '/config/' + horizonPointsFileName):
                msg = 'Horizon points file does not exist !'
                self.logger.warning('horizon points file does not exist')
            else:
                try:
                    with open(os.getcwd() + '/config/' + horizonPointsFileName) as f:
                        for line in f:
                            if ':' in line:
                                # model maker format
                                m = line.rstrip('\n').split(':')
                            else:
                                # carte du ciel / skychart format
                                m = line.rstrip('\n').split(' ')
                            point = (int(m[0]), int(m[1]))
                            hp.append(point)
                    f.close()
                except Exception as e:
                    msg = 'Error loading horizon points: {0}'.format(e)
                    self.logger.error('Error loading horizon points: {0}'.format(e))
                    return msg
            hp = sorted(hp, key=operator.itemgetter(0))
        if line_check:
            minAlt = int(line_value)
            if len(hp) == 0:
                hp = [(0, minAlt), (359, minAlt)]
        # is there is the mask not until 360, we do it
        if hp[len(hp)-1][0] < 360:
            hp.append((359, hp[len(hp)-1][1]))
        az_last = 0
        alt_last = 0
        for i in range(0, len(hp)):
            az_act = hp[i][0]
            alt_act = hp[i][1]
            if az_act > az_last:
                incline = (alt_act - alt_last) / (az_act - az_last)
                for j in range(az_last, az_act):
                    if line_check:
                        point = (j, max(int(alt_last + incline * (j - az_last)), minAlt))
                    else:
                        point = (j, int(alt_last + incline * (j - az_last)))
                    self.horizonPoints.append(point)
            else:
                self.horizonPoints.append(hp[i])
            az_last = az_act
            alt_last = alt_act
        return msg

    def isAboveHorizonLine(self, point):
        length = len(self.horizonPoints)
        if length > 0 and point[0] < length:
            if point[1] > self.horizonPoints[int(point[0])][1]:
                return True
            else:
                return False
        else:
            return True

    def deleteBelowHorizonLine(self):
        i = 0
        while i < len(self.RefinementPoints):
            if self.isAboveHorizonLine(self.RefinementPoints[i]):
                i += 1
            else:
                del self.RefinementPoints[i]

    def deletePoints(self):
        self.BasePoints = []
        self.RefinementPoints = []
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def loadBasePoints(self, filename):
        self.BasePoints, msg = self.loadModelPoints(filename, 'Base')
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def loadRefinementPoints(self, filename, horizonMask, sortPoints):
        self.RefinementPoints, msg = self.loadModelPoints(filename, 'Refinement')
        if horizonMask:
            self.deleteBelowHorizonLine()
        if sortPoints:
            self.sortPoints('Refinement')
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def generateDSOPoints(self, horizonMask, hours, numPoints, hoursPrev):
        if 'RaJNow' not in self.app.mount.data:
            return
        self.RefinementPoints = []
        ra = copy.copy(self.app.mount.data['RaJNow'])
        dec = copy.copy(self.app.mount.data['DecJNow'])
        for i in range(0, numPoints):
            ra = ra - float(i) * hours / numPoints - hoursPrev
            az, alt = self.transform.transformERFA(ra, dec, 1)
            if alt > 0:
                self.RefinementPoints.append((az, alt))
        if horizonMask:
            self.deleteBelowHorizonLine()
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def generateMaxPoints(self, horizonMask, sortPoints):
        west = []
        east = []
        for dec in range(-10, 90, 10):
            if dec < 30:
                step = -15
            elif dec < 70:
                step = -10
            else:
                step = -30
            for ha in range(120, -120, step):
                az, alt = self.transform.transformERFA(ha / 10, dec, 1)
                if alt > 0:
                    if az > 180:
                        east.append((az, alt))
                    else:
                        west.append((az, alt))
        self.RefinementPoints = west + east
        if horizonMask:
            self.deleteBelowHorizonLine()
        if sortPoints:
            self.sortPoints('Refinement')
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def generateNormalPoints(self, horizonMask, sortPoints):
        west = []
        east = []
        for dec in range(-15, 90, 15):
            if dec < 60:
                step = -10
            else:
                step = -20
            for ha in range(120, -120, step):
                az, alt = self.transform.transformERFA(ha / 10, dec, 1)
                if alt > 0:
                    if az > 180:
                        east.append((az, alt))
                    else:
                        west.append((az, alt))
        self.RefinementPoints = west + east
        if horizonMask:
            self.deleteBelowHorizonLine()
        if sortPoints:
            self.sortPoints('Refinement')
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def generateGridPoints(self, horizonMask, sortPoints, row, col, altMin, altMax):
        self.RefinementPoints = []
        for az in range(5, 360, int(360 / col)):
            for alt in range(altMin, altMax + 1, int((altMax - altMin) / (row - 1))):
                self.RefinementPoints.append((az, alt))
        if horizonMask:
            self.deleteBelowHorizonLine()
        if sortPoints:
            self.sortPoints('Refinement')
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)

    def generateBasePoints(self, az, alt):
        self.BasePoints = []
        for i in range(0, 3):
            azp = i * 120 + az
            if azp > 360:
                azp -= 360
            point = (azp, alt)
            self.BasePoints.append(point)
        self.app.workerModelingDispatcher.signalModelPointsRedraw.emit(True)