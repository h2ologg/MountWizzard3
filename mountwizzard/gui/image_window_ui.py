# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageDialog(object):
    def setupUi(self, ImageDialog):
        ImageDialog.setObjectName("ImageDialog")
        ImageDialog.resize(791, 641)
        font = QtGui.QFont()
        font.setFamily("Arial")
        ImageDialog.setFont(font)
        self.image = QtWidgets.QWidget(ImageDialog)
        self.image.setGeometry(QtCore.QRect(10, 115, 771, 516))
        self.image.setAutoFillBackground(True)
        self.image.setObjectName("image")
        self.btn_expose = QtWidgets.QPushButton(ImageDialog)
        self.btn_expose.setGeometry(QtCore.QRect(10, 10, 81, 26))
        self.btn_expose.setObjectName("btn_expose")
        self.groupBox_2 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(710, 10, 71, 86))
        self.groupBox_2.setObjectName("groupBox_2")
        self.btn_strechLow = QtWidgets.QRadioButton(self.groupBox_2)
        self.btn_strechLow.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.btn_strechLow.setObjectName("btn_strechLow")
        self.btn_strechMid = QtWidgets.QRadioButton(self.groupBox_2)
        self.btn_strechMid.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.btn_strechMid.setObjectName("btn_strechMid")
        self.btn_strechHigh = QtWidgets.QRadioButton(self.groupBox_2)
        self.btn_strechHigh.setGeometry(QtCore.QRect(10, 60, 61, 21))
        self.btn_strechHigh.setObjectName("btn_strechHigh")
        self.groupBox_3 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(630, 10, 71, 86))
        self.groupBox_3.setObjectName("groupBox_3")
        self.btn_size25 = QtWidgets.QRadioButton(self.groupBox_3)
        self.btn_size25.setGeometry(QtCore.QRect(10, 20, 61, 21))
        self.btn_size25.setObjectName("btn_size25")
        self.btn_size50 = QtWidgets.QRadioButton(self.groupBox_3)
        self.btn_size50.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.btn_size50.setObjectName("btn_size50")
        self.btn_size100 = QtWidgets.QRadioButton(self.groupBox_3)
        self.btn_size100.setGeometry(QtCore.QRect(10, 60, 61, 21))
        self.btn_size100.setObjectName("btn_size100")
        self.btn_solve = QtWidgets.QPushButton(ImageDialog)
        self.btn_solve.setGeometry(QtCore.QRect(10, 40, 81, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_solve.setFont(font)
        self.btn_solve.setObjectName("btn_solve")
        self.groupBox_4 = QtWidgets.QGroupBox(ImageDialog)
        self.groupBox_4.setGeometry(QtCore.QRect(540, 10, 81, 86))
        self.groupBox_4.setObjectName("groupBox_4")
        self.btn_colorGrey = QtWidgets.QRadioButton(self.groupBox_4)
        self.btn_colorGrey.setGeometry(QtCore.QRect(10, 20, 71, 21))
        self.btn_colorGrey.setObjectName("btn_colorGrey")
        self.btn_colorCool = QtWidgets.QRadioButton(self.groupBox_4)
        self.btn_colorCool.setGeometry(QtCore.QRect(10, 40, 71, 21))
        self.btn_colorCool.setObjectName("btn_colorCool")
        self.btn_colorRainbow = QtWidgets.QRadioButton(self.groupBox_4)
        self.btn_colorRainbow.setGeometry(QtCore.QRect(10, 60, 71, 21))
        self.btn_colorRainbow.setObjectName("btn_colorRainbow")
        self.cross4 = QtWidgets.QFrame(ImageDialog)
        self.cross4.setGeometry(QtCore.QRect(405, 390, 1, 231))
        self.cross4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross4.setFrameShape(QtWidgets.QFrame.VLine)
        self.cross4.setObjectName("cross4")
        self.cross2 = QtWidgets.QFrame(ImageDialog)
        self.cross2.setGeometry(QtCore.QRect(405, 120, 1, 231))
        self.cross2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross2.setFrameShape(QtWidgets.QFrame.VLine)
        self.cross2.setObjectName("cross2")
        self.cross1 = QtWidgets.QFrame(ImageDialog)
        self.cross1.setGeometry(QtCore.QRect(20, 370, 371, 1))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cross1.setFont(font)
        self.cross1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross1.setFrameShape(QtWidgets.QFrame.HLine)
        self.cross1.setObjectName("cross1")
        self.cross3 = QtWidgets.QFrame(ImageDialog)
        self.cross3.setGeometry(QtCore.QRect(420, 370, 351, 1))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cross3.setFont(font)
        self.cross3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.cross3.setFrameShape(QtWidgets.QFrame.HLine)
        self.cross3.setObjectName("cross3")
        self.imageBackground = QtWidgets.QLabel(ImageDialog)
        self.imageBackground.setGeometry(QtCore.QRect(0, 0, 790, 106))
        self.imageBackground.setText("")
        self.imageBackground.setObjectName("imageBackground")
        self.le_cameraExposureTime = QtWidgets.QLineEdit(ImageDialog)
        self.le_cameraExposureTime.setEnabled(False)
        self.le_cameraExposureTime.setGeometry(QtCore.QRect(500, 30, 31, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_cameraExposureTime.setFont(font)
        self.le_cameraExposureTime.setMouseTracking(False)
        self.le_cameraExposureTime.setAcceptDrops(False)
        self.le_cameraExposureTime.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_cameraExposureTime.setText("")
        self.le_cameraExposureTime.setMaxLength(15)
        self.le_cameraExposureTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_cameraExposureTime.setReadOnly(False)
        self.le_cameraExposureTime.setObjectName("le_cameraExposureTime")
        self.label_83 = QtWidgets.QLabel(ImageDialog)
        self.label_83.setGeometry(QtCore.QRect(410, 55, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_83.setFont(font)
        self.label_83.setObjectName("label_83")
        self.label_84 = QtWidgets.QLabel(ImageDialog)
        self.label_84.setGeometry(QtCore.QRect(410, 10, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_84.setFont(font)
        self.label_84.setObjectName("label_84")
        self.le_astrometryStatusText = QtWidgets.QLineEdit(ImageDialog)
        self.le_astrometryStatusText.setEnabled(False)
        self.le_astrometryStatusText.setGeometry(QtCore.QRect(410, 75, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.le_astrometryStatusText.setFont(font)
        self.le_astrometryStatusText.setMouseTracking(False)
        self.le_astrometryStatusText.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_astrometryStatusText.setAcceptDrops(False)
        self.le_astrometryStatusText.setText("")
        self.le_astrometryStatusText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_astrometryStatusText.setReadOnly(True)
        self.le_astrometryStatusText.setObjectName("le_astrometryStatusText")
        self.le_cameraStatusText = QtWidgets.QLineEdit(ImageDialog)
        self.le_cameraStatusText.setEnabled(False)
        self.le_cameraStatusText.setGeometry(QtCore.QRect(410, 30, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.le_cameraStatusText.setFont(font)
        self.le_cameraStatusText.setMouseTracking(False)
        self.le_cameraStatusText.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_cameraStatusText.setAcceptDrops(False)
        self.le_cameraStatusText.setText("")
        self.le_cameraStatusText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_cameraStatusText.setReadOnly(True)
        self.le_cameraStatusText.setObjectName("le_cameraStatusText")
        self.le_imageFile = QtWidgets.QLineEdit(ImageDialog)
        self.le_imageFile.setEnabled(False)
        self.le_imageFile.setGeometry(QtCore.QRect(100, 10, 206, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_imageFile.setFont(font)
        self.le_imageFile.setMouseTracking(False)
        self.le_imageFile.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_imageFile.setAcceptDrops(False)
        self.le_imageFile.setText("")
        self.le_imageFile.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_imageFile.setReadOnly(True)
        self.le_imageFile.setObjectName("le_imageFile")
        self.le_RaJ2000 = QtWidgets.QLineEdit(ImageDialog)
        self.le_RaJ2000.setEnabled(False)
        self.le_RaJ2000.setGeometry(QtCore.QRect(125, 40, 76, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_RaJ2000.setFont(font)
        self.le_RaJ2000.setMouseTracking(False)
        self.le_RaJ2000.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_RaJ2000.setAcceptDrops(False)
        self.le_RaJ2000.setText("")
        self.le_RaJ2000.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_RaJ2000.setReadOnly(True)
        self.le_RaJ2000.setObjectName("le_RaJ2000")
        self.le_DecJ2000 = QtWidgets.QLineEdit(ImageDialog)
        self.le_DecJ2000.setEnabled(False)
        self.le_DecJ2000.setGeometry(QtCore.QRect(230, 40, 76, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_DecJ2000.setFont(font)
        self.le_DecJ2000.setMouseTracking(False)
        self.le_DecJ2000.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_DecJ2000.setAcceptDrops(False)
        self.le_DecJ2000.setText("")
        self.le_DecJ2000.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.le_DecJ2000.setReadOnly(True)
        self.le_DecJ2000.setObjectName("le_DecJ2000")
        self.btn_loadFits = QtWidgets.QPushButton(ImageDialog)
        self.btn_loadFits.setEnabled(True)
        self.btn_loadFits.setGeometry(QtCore.QRect(125, 70, 81, 26))
        self.btn_loadFits.setObjectName("btn_loadFits")
        self.label_85 = QtWidgets.QLabel(ImageDialog)
        self.label_85.setGeometry(QtCore.QRect(100, 40, 26, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_85.setFont(font)
        self.label_85.setObjectName("label_85")
        self.label_86 = QtWidgets.QLabel(ImageDialog)
        self.label_86.setGeometry(QtCore.QRect(205, 40, 26, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_86.setFont(font)
        self.label_86.setObjectName("label_86")
        self.le_astrometrySolvingTime = QtWidgets.QLineEdit(ImageDialog)
        self.le_astrometrySolvingTime.setEnabled(False)
        self.le_astrometrySolvingTime.setGeometry(QtCore.QRect(500, 75, 31, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_astrometrySolvingTime.setFont(font)
        self.le_astrometrySolvingTime.setMouseTracking(False)
        self.le_astrometrySolvingTime.setAcceptDrops(False)
        self.le_astrometrySolvingTime.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_astrometrySolvingTime.setText("")
        self.le_astrometrySolvingTime.setMaxLength(15)
        self.le_astrometrySolvingTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_astrometrySolvingTime.setReadOnly(False)
        self.le_astrometrySolvingTime.setObjectName("le_astrometrySolvingTime")
        self.btn_cancel = QtWidgets.QPushButton(ImageDialog)
        self.btn_cancel.setGeometry(QtCore.QRect(10, 70, 81, 26))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.checkShowCrosshairs = QtWidgets.QCheckBox(ImageDialog)
        self.checkShowCrosshairs.setGeometry(QtCore.QRect(220, 75, 86, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkShowCrosshairs.setFont(font)
        self.checkShowCrosshairs.setChecked(False)
        self.checkShowCrosshairs.setObjectName("checkShowCrosshairs")
        self.imageBackground.raise_()
        self.image.raise_()
        self.btn_expose.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.btn_solve.raise_()
        self.groupBox_4.raise_()
        self.cross4.raise_()
        self.cross2.raise_()
        self.cross1.raise_()
        self.cross3.raise_()
        self.le_cameraExposureTime.raise_()
        self.label_83.raise_()
        self.label_84.raise_()
        self.le_astrometryStatusText.raise_()
        self.le_cameraStatusText.raise_()
        self.le_imageFile.raise_()
        self.le_RaJ2000.raise_()
        self.le_DecJ2000.raise_()
        self.btn_loadFits.raise_()
        self.label_85.raise_()
        self.label_86.raise_()
        self.le_astrometrySolvingTime.raise_()
        self.btn_cancel.raise_()
        self.checkShowCrosshairs.raise_()

        self.retranslateUi(ImageDialog)
        QtCore.QMetaObject.connectSlotsByName(ImageDialog)

    def retranslateUi(self, ImageDialog):
        _translate = QtCore.QCoreApplication.translate
        ImageDialog.setWindowTitle(_translate("ImageDialog", "Imaging"))
        self.btn_expose.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Single exposure</p></body></html>"))
        self.btn_expose.setText(_translate("ImageDialog", "Expose One"))
        self.groupBox_2.setTitle(_translate("ImageDialog", "Strech"))
        self.btn_strechLow.setText(_translate("ImageDialog", "Low"))
        self.btn_strechMid.setText(_translate("ImageDialog", "Mid"))
        self.btn_strechHigh.setText(_translate("ImageDialog", "High"))
        self.groupBox_3.setTitle(_translate("ImageDialog", "Zoom"))
        self.btn_size25.setText(_translate("ImageDialog", "4x"))
        self.btn_size50.setText(_translate("ImageDialog", "2x"))
        self.btn_size100.setText(_translate("ImageDialog", "1x"))
        self.btn_solve.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Single plate solve of the actual image</p></body></html>"))
        self.btn_solve.setText(_translate("ImageDialog", "Solve"))
        self.groupBox_4.setTitle(_translate("ImageDialog", "Colors"))
        self.btn_colorGrey.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Color scheme black /white</p></body></html>"))
        self.btn_colorGrey.setText(_translate("ImageDialog", "Grey"))
        self.btn_colorCool.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Color scheme red/blue</p></body></html>"))
        self.btn_colorCool.setText(_translate("ImageDialog", "Cool"))
        self.btn_colorRainbow.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Color scheme rainbow</p></body></html>"))
        self.btn_colorRainbow.setText(_translate("ImageDialog", "Rainbow"))
        self.imageBackground.setProperty("color", _translate("ImageDialog", "blue"))
        self.le_cameraExposureTime.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Time left for image integration</p></body></html>"))
        self.label_83.setText(_translate("ImageDialog", "Astrometry"))
        self.label_84.setText(_translate("ImageDialog", "Camera"))
        self.le_astrometryStatusText.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Status feedback from astrometry</span></p></body></html>"))
        self.le_cameraStatusText.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Status feedback from camera</span></p></body></html>"))
        self.le_imageFile.setToolTip(_translate("ImageDialog", "Status feedback from mount "))
        self.le_RaJ2000.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved RA of image in J2000 coordinates</span></p></body></html>"))
        self.le_DecJ2000.setToolTip(_translate("ImageDialog", "<html><head/><body><p><span style=\" font-weight:400;\">Shows the solved DEC of image in J2000 coordinates</span></p></body></html>"))
        self.btn_loadFits.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Single exposure</p></body></html>"))
        self.btn_loadFits.setText(_translate("ImageDialog", "Show FITS"))
        self.label_85.setText(_translate("ImageDialog", "RA"))
        self.label_86.setText(_translate("ImageDialog", "Dec"))
        self.le_astrometrySolvingTime.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Time elapsed for plate solving</p></body></html>"))
        self.btn_cancel.setToolTip(_translate("ImageDialog", "<html><head/><body><p>Cancels an imaging or plate solving action</p></body></html>"))
        self.btn_cancel.setText(_translate("ImageDialog", "Cancel"))
        self.checkShowCrosshairs.setToolTip(_translate("ImageDialog", "Use Highspeed download of CCD camera if availabe"))
        self.checkShowCrosshairs.setText(_translate("ImageDialog", "Crosshairs"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImageDialog = QtWidgets.QWidget()
    ui = Ui_ImageDialog()
    ui.setupUi(ImageDialog)
    ImageDialog.show()
    sys.exit(app.exec_())

