from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsPixmapItem,QDialog,QMessageBox,QWidget
from PyQt5.QtGui import QImage, QPixmap, QCursor
from utils.cal import *
import os

from views.Ui_MainWindow import Ui_MainWindow
from utils.plot import *

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.imgpath = None
        self.DTclassname = None
        self.DTXYWH = None 
        self.DTconfidence = None
        self.GT_xyxy = None
        self.GTclassname = None
        self.GTXYWH = None 
        self.GT_xyxy= None
        self.h = None
        self.w = None
        self.img = None
        self.showDT = True
        self.showGT = True
        

    def setup_control(self):
        # menubar
        self.ui.actionOpen_Dir.triggered.connect(self.open_folder)
        self.ui.FileListWidget.itemClicked.connect(self.FileListItemClick)
        # slider
        self.ui.ConfidenceSlider.valueChanged.connect(self.confidence_change)
        # button
        self.ui.ShowGroundTruthButton.clicked.connect(self.hide_show_GT)
        self.ui.ShowDetectionButton.clicked.connect(self.hide_show_DT)

        


    # === MenuBar action :OpenDir ===
    def open_folder(self):
        supported_format = ['.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg', '.jpe', '.jp2', '.tiff', '.tif', '.png']
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder", "./")
        if folder_path:
            UIFileList = self.ui.FileListWidget
            self.ui.FileListWidget.clear()
            for fileName in os.listdir(folder_path):
                supportedFlag = False
                _, endname = os.path.splitext(fileName)
                if endname in supported_format:
                    supportedFlag = True
                if supportedFlag :
                    item = QtWidgets.QListWidgetItem()
                    item.setText(fileName)
                    item.setData(4, folder_path)  
                    UIFileList.addItem(item)
        else: 
            return
    
    # === click image file === 
    def FileListItemClick(self, item):
        self.all_view_clear()
        self.imgpath = os.path.join(item.data(4), item.text())
        # print(filepath)
        self.img, self.h, self.w = readImage(self.imgpath)
        # print(h,w)
        view = self.ui.DetectionView
        plot_original(view, self.img)

        # plot DT
        self.DTclassname, self.DTXYWH, self.DTconfidence = read_detection(self.imgpath)
        self.set_conf_hist(self.DTconfidence)
        if self.showDT:
            plot_detection(view, [self.h, self.w], self.DTclassname, self.DTXYWH, self.DTconfidence, threshold=self.ui.ConfidenceSlider.value()/100)

        try:
            # plot GT
            self.GTclassname, self.GTXYWH = read_groundTruth(self.imgpath)
            if self.showGT:
                plot_groundTruth(view, [self.h, self.w], self.GTclassname, self.GTXYWH)


            # cal PR
            self.GT_xyxy = xywhn2xyxy(x=self.GTXYWH, w=self.w, h=self.h)
            self.DT_xyxy = xywhn2xyxy(x=self.DTXYWH, w=self.w, h=self.h)
            P, R = self.set_PR(self.ui, self.GT_xyxy, self.DT_xyxy, self.DTconfidence)
            self.set_PR_curve(self.ui, P, R)

            # set F1
            self.set_F1_score(self.ui, P, R)
            
            # mAP@55:95
            self.set_mAP55to95(self.ui, self.GT_xyxy, self.DT_xyxy, self.DTconfidence)
        except:
            print("There are no groundtruth...")

    def confidence_change(self):
        confidence = self.ui.ConfidenceSlider.value()
        self.ui.ScoreLabel.setText(str(confidence/100))
        self.replot()
        

    def hide_show_GT(self):
        self.showGT = not self.showGT
        for item in self.ui.DetectionView.scene.items():
            if isinstance(item, MyRectItem):
                if item.type == 'GT':
                    if self.showGT:
                        item.setVisible(True)
                    else:
                        item.setVisible(False)
        if self.showGT:
            self.ui.ShowGroundTruthButton.setText("Hide Groundtruth")
        else:
            self.ui.ShowGroundTruthButton.setText("Show Groundtruth")


    def hide_show_DT(self):
        self.showDT = not self.showDT
        for item in self.ui.DetectionView.scene.items():
            if isinstance(item, MyRectItem):
                if item.type == 'DT':
                    if self.showDT:
                        item.setVisible(True)
                    else:
                        item.setVisible(False)
        if self.showDT:
            self.ui.ShowDetectionButton.setText("Hide Detection")
        else:
            self.ui.ShowDetectionButton.setText("Show Detection")

    def replot(self):
        view = self.ui.DetectionView
        self.removeDT()
        # plot_original(view, self.img)
        if self.showDT:
            plot_detection(view, [self.h,self.w], self.DTclassname, self.DTXYWH, self.DTconfidence, threshold=self.ui.ConfidenceSlider.value()/100)
        

    def removeDT(self):
        for item in self.ui.DetectionView.scene.items():
            if isinstance(item, MyRectItem) and item.type == 'DT':
                self.ui.DetectionView.scene.removeItem(item)

    # ============= P and R vs conf ==============
    def set_PR(self, mainview, GT_xyxy, DT_xyxy, DT_confidence):
        P = []
        R = []
        for ch_index in range(len(DT_xyxy)):
            _, _, _, tmpP, tmpR = FindPR(GT_xyxy, DT_xyxy, DT_confidence, DT_confidence[ch_index], 0.5)
            P.append(tmpP)
            R.append(tmpR)
        plot_P_R_conf(mainview.P_R_view, P, R, DT_confidence)
        return P, R

    # ============= conf histogram  ==============
    def set_conf_hist(self, data):
        plot_conf_hist(self.ui.conf_hist_view, data)

    # ============= PR curve        ==============
    def set_PR_curve(self, mainview, P, R):
        plot_PR_curve(mainview.PR_view, P, R)
    # ============= f1 vs conf      ==============
    def set_F1_score(self, mainview, P, R):
        plot_F1(mainview.F1_view, P, R, self.DTconfidence)
    # =============       mAP@0.5   ==============
    # ============= mAP@0.55:0.95   ==============
    def set_mAP55to95(self, mainview, GT_xyxy, DT_xyxy, DT_confidence):
        AP =[]
        for cond_thre in np.linspace(0.55,0.95,9):
            P = []
            R = []
            for ch_index in range(len(DT_xyxy)):
                _, _, _, tmpP, tmpR = FindPR(GT_xyxy, DT_xyxy, DT_confidence, DT_confidence[ch_index], cond_thre)
                P.append(tmpP)
                R.append(tmpR)
            AP.append(ComputeAP(P, R))
        plot_mAP55to95(mainview.mAP55to95_view, AP)


    def all_view_clear(self):
        self.ui.DetectionView.scene.clear()
        self.ui.P_R_view.scene.clear()
        self.ui.PR_view.scene.clear()
        self.ui.conf_hist_view.scene.clear()
        self.ui.mAP05_view.scene.clear()
        self.ui.F1_view.scene.clear()
        self.ui.mAP55to95_view.scene.clear()