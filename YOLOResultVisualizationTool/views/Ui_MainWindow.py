# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from utils.plot import GraphicView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DetectionVLayout = QtWidgets.QVBoxLayout()
        self.DetectionVLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.DetectionVLayout.setSpacing(0)


        # === font of toolButton ===
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        # ==========================

        # ===== detection =====
        self.DetectionVLayout.setObjectName("DetectionVLayout")
        # --- label ---
        self.DetectionLabel = QtWidgets.QLabel(self.centralwidget)
        self.DetectionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DetectionLabel.setObjectName("DetectionLabel")
        self.DetectionLabel.setFont(font)
        self.DetectionVLayout.addWidget(self.DetectionLabel)

        # --- view ---
        self.DetectionView = GraphicView(self.centralwidget)
        self.DetectionView.setObjectName("DetectionView")
        self.DetectionVLayout.addWidget(self.DetectionView)
        self.DetectionVLayout.setStretch(0, 1)
        self.DetectionVLayout.setStretch(1, 19)
        self.horizontalLayout.addLayout(self.DetectionVLayout)
        # ====================

        # ===== Analysis ===== 
        self.AnalysisVLayout = QtWidgets.QVBoxLayout()
        self.AnalysisVLayout.setObjectName("AnalysisVLayout")
        # --- label ---
        self.AnalysisLabel = QtWidgets.QLabel(self.centralwidget)
        self.AnalysisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AnalysisLabel.setObjectName("AnalysisLabel")
        self.AnalysisLabel.setFont(font)
        self.AnalysisVLayout.addWidget(self.AnalysisLabel)

        # --- view (left) ---
        self.AnalysisHLayout = QtWidgets.QHBoxLayout()
        self.AnalysisHLayout.setObjectName("AnalysisHLayout")
        self.AnalysisHLayoutLeft = QtWidgets.QVBoxLayout()
        self.AnalysisHLayoutLeft.setSpacing(0)
        self.AnalysisHLayoutLeft.setObjectName("AnalysisHLayoutLeft")

        # --- P and R vs confidence view ---
        self.P_R_view = GraphicView(self.centralwidget)
        self.P_R_view.setObjectName("P_R_view")
        self.AnalysisHLayoutLeft.addWidget(self.P_R_view)

        # --- P vs R view ---
        self.PR_view = GraphicView(self.centralwidget)
        self.PR_view.setObjectName("PR_view")
        self.AnalysisHLayoutLeft.addWidget(self.PR_view)

        # --- mAP@0.5 ---
        self.mAP05_view = GraphicView(self.centralwidget)
        self.mAP05_view.setObjectName("mAP05_view")
        self.AnalysisHLayoutLeft.addWidget(self.mAP05_view)
        self.AnalysisHLayout.addLayout(self.AnalysisHLayoutLeft)

        # --- view (right) ---
        self.AnalysisHLayoutRight = QtWidgets.QVBoxLayout()
        self.AnalysisHLayoutRight.setSpacing(0)
        self.AnalysisHLayoutRight.setObjectName("AnalysisHLayoutRight")

        # --- confidence hist view ---
        self.conf_hist_view = GraphicView(self.centralwidget)
        self.conf_hist_view.setObjectName("conf_hist_view")
        self.AnalysisHLayoutRight.addWidget(self.conf_hist_view)

        # --- F1 vs confidence view ---
        self.F1_view = GraphicView(self.centralwidget)
        self.F1_view.setObjectName("F1_view")
        self.AnalysisHLayoutRight.addWidget(self.F1_view)

        # --- mAP@0.5:0.95 ---
        self.mAP55to95_view = GraphicView(self.centralwidget)
        self.mAP55to95_view.setObjectName("mAP55to95_view")
        self.AnalysisHLayoutRight.addWidget(self.mAP55to95_view)
        self.AnalysisHLayout.addLayout(self.AnalysisHLayoutRight)
        self.AnalysisVLayout.addLayout(self.AnalysisHLayout)
        self.horizontalLayout.addLayout(self.AnalysisVLayout)
        # ====================

        # ===== Control Layout ======
        self.ControlVLayout = QtWidgets.QVBoxLayout()
        self.ControlVLayout.setObjectName("ControlVLayout")
        self.ConfidenceHLayout = QtWidgets.QHBoxLayout()
        self.ConfidenceHLayout.setObjectName("ConfidenceHLayout")
        
        # --- confidence ---
        self.ConfidenceLabel = QtWidgets.QLabel(self.centralwidget)
        self.ConfidenceLabel.setScaledContents(False)
        self.ConfidenceLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ConfidenceLabel.setOpenExternalLinks(False)
        self.ConfidenceLabel.setObjectName("ConfidenceLabel")
        self.ConfidenceLabel.setFont(font)
        self.ConfidenceHLayout.addWidget(self.ConfidenceLabel)

        # --- confidence score ---
        self.ScoreLabel = QtWidgets.QLabel(self.centralwidget)
        self.ScoreLabel.setObjectName("ScoreLabel")
        self.ScoreLabel.setFont(font)
        self.ConfidenceHLayout.addWidget(self.ScoreLabel)
        self.ConfidenceHLayout.setStretch(0, 6)
        self.ConfidenceHLayout.setStretch(1, 4)
        self.ControlVLayout.addLayout(self.ConfidenceHLayout)

        # --- confidence slider ---
        self.ConfidenceSlider = QtWidgets.QSlider(self.centralwidget)
        self.ConfidenceSlider.setMaximum(100)
        self.ConfidenceSlider.setSingleStep(1)
        self.ConfidenceSlider.setPageStep(8)
        self.ConfidenceSlider.setProperty("value", 30)
        self.ConfidenceSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ConfidenceSlider.setInvertedAppearance(False)
        self.ConfidenceSlider.setInvertedControls(False)
        self.ConfidenceSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.ConfidenceSlider.setTickInterval(10)
        self.ConfidenceSlider.setObjectName("ConfidenceSlider")
        self.ControlVLayout.addWidget(self.ConfidenceSlider)

        # --- show or hide GroundTruth ---
        self.ShowGroundTruthButton = QtWidgets.QPushButton(self.centralwidget)
        self.ShowGroundTruthButton.setObjectName("ShowGroundTruthButton")
        self.ShowGroundTruthButton.setFont(font)
        self.ControlVLayout.addWidget(self.ShowGroundTruthButton)

        # --- show or hide Detection ---
        self.ShowDetectionButton = QtWidgets.QPushButton(self.centralwidget)
        self.ShowDetectionButton.setObjectName("ShowDetectionButton")
        self.ShowDetectionButton.setFont(font)
        self.ControlVLayout.addWidget(self.ShowDetectionButton)


        # --- FileList ---
        self.FileListLabel = QtWidgets.QLabel(self.centralwidget)
        self.FileListLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FileListLabel.setObjectName("FileListLabel")
        self.FileListLabel.setFont(font)
        self.ControlVLayout.addWidget(self.FileListLabel)

        self.FileListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.FileListWidget.setObjectName("FileListWidget")
        self.ControlVLayout.addWidget(self.FileListWidget)
        self.ControlVLayout.setStretch(0, 1)
        self.ControlVLayout.setStretch(5, 7)

        self.horizontalLayout.addLayout(self.ControlVLayout)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 2)

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Dir = QtWidgets.QAction(MainWindow)
        self.actionOpen_Dir.setObjectName("actionOpen_Dir")
        self.actionExport_Analysis = QtWidgets.QAction(MainWindow)
        self.actionExport_Analysis.setObjectName("actionExport_Analysis")
        self.menuFile.addAction(self.actionOpen_Dir)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_Analysis)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DetectionLabel.setText(_translate("MainWindow", "Detection"))
        self.AnalysisLabel.setText(_translate("MainWindow", "Analysis"))
        self.ConfidenceLabel.setText(_translate("MainWindow", "Confidence Threshold"))
        self.ScoreLabel.setText(str(self.ConfidenceSlider.value()/100))
        self.ShowGroundTruthButton.setText(_translate("MainWindow", "Hide GroundTruth"))
        self.ShowDetectionButton.setText(_translate("MainWindow", "Hide Detection"))
        self.FileListLabel.setText(_translate("MainWindow", "FileList"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_Dir.setText(_translate("MainWindow", "Open Dir"))
        self.actionExport_Analysis.setText(_translate("MainWindow", "Export Analysis"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
