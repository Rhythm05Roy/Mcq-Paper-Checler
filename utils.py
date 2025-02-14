import cv2
import numpy as np

def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def rectContour(contours):
    ractangle = []
    for i in contours:
        area = cv2.contourArea(i)
        #print('Area',area)
        if area > 50:
            perameter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*perameter, True)
            # print('Corner Points',len(approx))
            if len(approx) == 4:
                ractangle.append(i)

    ractangle = sorted(ractangle, key = cv2.contourArea,reverse=True)
    return ractangle

def getCornerPoints(contours):
    perameter = cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, 0.02*perameter, True)
    return approx

def reorder(mypoints):
    mypoints = mypoints.reshape((4,2))
    mypointsNew = np.zeros((4,1,2),np.int32)
    add = mypoints.sum(1)
    # print(add)
    # print(mypoints)
    mypointsNew[0] = mypoints[np.argmin(add)] # [ 0, 0 ]
    mypointsNew[3] = mypoints[np.argmax(add)] # [ w, h ]
    diff = np.diff(mypoints,axis=1) 
    mypointsNew[1] = mypoints[np.argmin(diff)] # [ w, 0 ]
    mypointsNew[2] = mypoints[np.argmax(diff)] # [ 0, h ]
    # print(diff)
    return mypointsNew

def splitBoxes(img):
    rows = np.vsplit(img,5)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,5)
        for box in cols:
            boxes.append(box)
            # cv2.imshow('box',box)
    # cv2.imshow('row1',rows[0])
    return boxes

def showAnswers(img, myIndex, grading,ans,questions,choices):
    secW = img.shape[1] // questions
    secH = img.shape[0] // choices

    for x in range(0,questions):
        myAns = myIndex[x]
        cX = (myAns * secW) + secW//2
        cY = (x*secH) + secH//2
        if grading[x] == 1:
            myColor = (0,255,0)
        else:
            myColor = (0,0,255)
            correctAns = ans[x]
            cv2.circle(img, ((correctAns*secW)+secW//2,(x*secH)+secH//2),35,(0,255,0),cv2.FILLED)
        cv2.circle(img,(cX,cY),35,myColor,cv2.FILLED)
    
    return img