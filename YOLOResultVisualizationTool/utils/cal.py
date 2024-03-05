import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import auc

import math
import os

import cv2 as cv
import numpy as np
import pandas as pd




def isCollide(xyxy1, xyxy2):
    bbox1_xmin = xyxy1[0]
    bbox1_ymin = xyxy1[1]
    bbox1_xmax = xyxy1[2]
    bbox1_ymax = xyxy1[3]
    bbox2_xmin = xyxy2[0]
    bbox2_ymin = xyxy2[1]
    bbox2_xmax = xyxy2[2]
    bbox2_ymax = xyxy2[3]
    return not ((bbox1_xmax < bbox2_xmin) or (bbox1_xmin > bbox2_xmax) or (bbox1_ymax < bbox2_ymin) or (bbox1_ymin > bbox2_ymax))

def xyxyIou(xyxy1, xyxy2):
    # xyxy format
    # determine the coordinates of the intersection rectangle
    x_left = max(xyxy1[0], xyxy2[0])
    y_top = max(xyxy1[1], xyxy2[1])
    x_right = min(xyxy1[2], xyxy2[2])
    y_bottom = min(xyxy1[3], xyxy2[3])

    # no collision
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    coArea = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    Area1 = (xyxy1[2] - xyxy1[0]) * (xyxy1[3] - xyxy1[1])
    Area2 = (xyxy2[2] - xyxy2[0]) * (xyxy2[3] - xyxy2[1])

    iou = coArea / float(Area1 + Area2 - coArea)
    return iou

def ComputeAP(P, R):
    AP = auc(R,P)
    return AP

def ComputeF1(P, R):
    F1=[]
    for pp, rr in zip(P,R):
        F1.append(2/(1/pp + 1/rr))
    return F1

def FindPR(GTxyxy, DTxyxy, conf, conf_thre, iou_thre):
    GTresult = np.zeros(len(GTxyxy))
    DTresult = np.zeros(len(DTxyxy))
    for dt_index, dt in enumerate(DTxyxy):
        if conf[dt_index] >= conf_thre:
            for gt_index, gt in enumerate(GTxyxy):
                if (not GTresult[gt_index]) and xyxyIou(dt, gt) >= iou_thre:
                    GTresult[gt_index] = 1
                    DTresult[dt_index] = 1
                    break
        else:
            DTresult[dt_index] = -1
    TP = list(GTresult).count(1)
    FP = list(DTresult).count(0)
    FN = list(GTresult).count(0)
    P = np.float64(TP/(TP+FP)) 
    R = np.float64(TP/(TP+FN)) 
    return TP, FP, FN, P, R


