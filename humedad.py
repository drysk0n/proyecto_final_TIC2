from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_hum(object):
    def setupUi(self, hum):
        hum.setObjectName("hum")
        hum.resize(615, 589)
        self.title_hum = QtWidgets.QLabel(parent=hum)
        self.title_hum.setGeometry(QtCore.QRect(160, 40, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_hum.setFont(font)
        self.title_hum.setObjectName("title_hum")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=hum)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 90, 521, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.graf_hum = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.graf_hum.setContentsMargins(0, 0, 0, 0)
        self.graf_hum.setObjectName("graf_hum")

        self.retranslateUi(hum)
        QtCore.QMetaObject.connectSlotsByName(hum)

    def retranslateUi(self, hum):
        _translate = QtCore.QCoreApplication.translate
        hum.setWindowTitle(_translate("hum", "Form"))
        self.title_hum.setText(_translate("hum", "Gráficos de humedad"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    hum = QtWidgets.QWidget()
    ui = Ui_hum()
    ui.setupUi(hum)
    hum.show()
    sys.exit(app.exec())
