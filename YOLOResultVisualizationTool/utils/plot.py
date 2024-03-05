import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .cal import *

from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsPixmapItem, QGraphicsView, QGraphicsPathItem
from PyQt5.QtGui import QWheelEvent, QPen, QColor, QBrush, QPainter
from PyQt5.QtGui import QImage, QPixmap, QCursor, QPainterPath


class MyScene(QGraphicsScene):
    def __init__(self):
        super(MyScene, self).__init__(parent=None) # 初始化 QGraphicsScene
        self.setSceneRect(0,0,100,100) # 預設大小，載入檔案後會改大小

    def wheelEvent(self, event: QWheelEvent):
        zoom_in_factor = 1.1
        zoom_out_factor = 0.9
        # 根據滾輪的方向進行放大或縮小
        if event.delta() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        # 更新 QGraphicsView 的縮放比例
        view = self.views()[0]  # 假設只有一個 QGraphicsView
        view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        view.scale(zoom_factor, zoom_factor)

class GraphicView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)  # 禁用右鍵選單
        try:
            self.scene = MyScene()  # 設置管理QgraphicsItems的場景
            self.setAlignment(Qt.AlignTop | Qt.AlignCenter) 
            self.setScene(self.scene) 
        except Exception as e:
            print(e)

class MyRectItem(QGraphicsPathItem):
    def __init__(self, x1, y1, x2, y2, color=QColor(0, 255, 0), conf=1.0, type='GT' ,parent=None):
        super().__init__(parent)
        self.conf = conf
        self.type = type
        self.pen = QPen(color)
        self.pen.setWidth(3)
        self.brush = QBrush(QColor(0, 0, 0, 0))
        self.path = QPainterPath()
        self.path.moveTo(QPointF(x1, y1))
        self.path.lineTo(QPointF(x2, y1))
        self.path.lineTo(QPointF(x2, y2))
        self.path.lineTo(QPointF(x1, y2))
        self.path.closeSubpath()
        self.setPath(self.path)
        self.setPen(self.pen)
        self.setBrush(self.brush)

def read_yolov7_XYWH(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    classname = []
    XYWH = []
    confidence = []
    # Strips the newline character
    for line in Lines:
        # print("Line{}: {}".format(count, line.strip()))
        temp = line.split()
        classname.append(int(temp[0]))
        XYWH.append([float(x) for x in temp[1:5]])
        try:
            confidence.append(float(temp[5]))
        except:
            confidence=[]

    return classname, XYWH, confidence

def xyxy2xywhn(x, w=320, h=320):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] where xy1=top-left, xy2=bottom-right
    x = np.array(x)
    y = np.copy(x)
    if len(x):
        y[:, 0] = (x[:, 0] + x[:, 2]) / (2*w)  # x center
        y[:, 1] = (x[:, 1] + x[:, 3]) / (2*h)  # y center
        y[:, 2] = (x[:, 2] - x[:, 0]) / w  # width
        y[:, 3] = (x[:, 3] - x[:, 1]) / h  # height
    return y

def xywhn2xyxy(x, w=320, h=320, padw=0, padh=0):
    # Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    x = np.array(x)
    y = np.copy(x)
    if len(x):
        y[:, 0] = w * (x[:, 0] - x[:, 2] / 2) + padw  # top left x
        y[:, 1] = h * (x[:, 1] - x[:, 3] / 2) + padh  # top left y
        y[:, 2] = w * (x[:, 0] + x[:, 2] / 2) + padw  # bottom right x
        y[:, 3] = h * (x[:, 1] + x[:, 3] / 2) + padh  # bottom right y
    return y

def readImage(filename):
    # read an image and return RGB
    img = cv.imread(filename)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    height = img.shape[0]
    width = img.shape[1]
    return img, height, width

def plot_original(view, img):
    h, w, _ = img.shape
    img[0, : , :] = 0
    img[h-1, : ,:] = 0
    img[:, w-1, :] = 0
    img[:, 0, :] = 0
    # set QImage
    qImg = QImage(img, w, h, 3 * w, QImage.Format_RGB888)
    # set QPixmanp
    pix = QPixmap.fromImage(qImg)
    imgItem = QGraphicsPixmapItem(pix)
    view.scene.clear()
    view.scene.setSceneRect(QRectF(0, 0, w, h))
    view.scene.addItem(imgItem)
    view.setAlignment(Qt.AlignTop | Qt.AlignCenter)

def read_detection(imgPath):
    _, endname = os.path.splitext(imgPath)
    DT_directory = os.getcwd()+'/YOLOResultVisualizationTool/dataset/label/detect/'
    DT_path = os.path.basename(imgPath).replace(endname, '.txt')
    DT_path = os.path.join(DT_directory, DT_path)
    classname, XYWH, confidence = read_yolov7_XYWH(DT_path)
    return classname, XYWH, confidence
    
def plot_detection(view, imgsize, classname, XYWH, confidence, threshold):
    h = imgsize[0]
    w = imgsize[1]
    XYXY = xywhn2xyxy(XYWH,w,h)
    for cl, bbox, cs in zip(classname, XYXY, confidence):
        if cl==0:
            tmp = MyRectItem(bbox[0], bbox[1], bbox[2], bbox[3], conf= cs, type='DT')
            if cs >= threshold:
                view.scene.addItem(tmp)

def read_groundTruth(imgPath):
    _, endname = os.path.splitext(imgPath)
    DT_directory = os.getcwd()+'/YOLOResultVisualizationTool/dataset/label/groundtruth/'
    DT_path = os.path.basename(imgPath).replace(endname, '.txt')
    DT_path = os.path.join(DT_directory, DT_path)
    classname, XYWH, confidence = read_yolov7_XYWH(DT_path)
    return classname, XYWH

def plot_groundTruth(view, imgsize, classname, XYWH):
    h = imgsize[0]
    w = imgsize[1]
    XYXY = xywhn2xyxy(XYWH,w,h)
    for cl, bbox in zip(classname, XYXY):
        if cl==0:
            tmp = MyRectItem(bbox[0], bbox[1], bbox[2], bbox[3], color=QColor(255,0,0))
            view.scene.addItem(tmp)


# conf hist
def plot_conf_hist(view, conf):
    figure = Figure(figsize=(2,2))
    axes = figure.gca()
    axes.set_title("Confidence")
    axes.hist(conf, bins=np.linspace(0,1,11), color='blue', edgecolor='black')
    axes.grid(True)

    canvas = FigureCanvas(figure)
    proxy_widget = view.scene.addWidget(canvas)
    view.setAlignment(Qt.AlignLeft | Qt.AlignTop) 

# # PvsConf
def plot_P_R_conf(view, P, R, conf):
    figure = Figure(figsize=(2,2))
    axes = figure.gca()
    axes.set_title("P and R")
    axes.plot(conf, P, "-r", label="P")
    axes.plot(conf, R, "-b", label="R")
    axes.legend()
    axes.set_xlim([0,1])
    axes.set_ylim([0,1])
    axes.grid(True)

    canvas = FigureCanvas(figure)
    proxy_widget = view.scene.addWidget(canvas)
    view.setAlignment(Qt.AlignLeft | Qt.AlignTop) 

# AP (PR)
def plot_PR_curve(view, P, R):
    figure = Figure(figsize=(2,2))
    axes = figure.gca()
    axes.set_title(f"AP=%.3f" %(ComputeAP(P,R)))
    axes.plot(R, P, "-r")
    axes.set_xlim([0,1])
    axes.set_ylim([0,1])
    axes.grid(True)

    canvas = FigureCanvas(figure)
    proxy_widget = view.scene.addWidget(canvas)
    view.setAlignment(Qt.AlignLeft | Qt.AlignTop) 

# F1
def plot_F1(view, P, R, DTconfidence):
    figure = Figure(figsize=(2,2))
    axes = figure.gca()
    F1 = ComputeF1(P, R)
    axes.set_title("F1")
    axes.plot(DTconfidence, F1, "-r")
    axes.set_xlim([0,1])
    axes.set_ylim([0,1])
    axes.grid(True)

    canvas = FigureCanvas(figure)
    proxy_widget = view.scene.addWidget(canvas)
    view.setAlignment(Qt.AlignLeft | Qt.AlignTop) 


# mAP@55:95
def plot_mAP55to95(view, AP):
    figure = Figure(figsize=(2,2))
    axes = figure.gca()
    axes.set_title("mAP@55:95")
    axes.plot(np.linspace(0.55,0.95,9), AP, "-r")
    axes.set_xlim([0.5,1])
    axes.set_ylim([0,1])
    axes.grid(True)

    canvas = FigureCanvas(figure)
    proxy_widget = view.scene.addWidget(canvas)
    view.setAlignment(Qt.AlignLeft | Qt.AlignTop) 