import heapq as heaps
import cv2 as cv2
import numpy as np
import os
import json

class imagereg():
    
    
    x=0
    y=0
    imageID_A='11'
    imageID_B='12'
    imageID_C='13'
    imageID_D='14'
    imageID_E='15'
    imageID_1='6'
    imageID_2='7'
    imageID_3='8'
    imageID_4='9'
    imageID_5='10'
    imageID_UA='1'
    imageID_DA='2'
    imageID_RA='3'
    imageID_LA='4'
    imageID_CIR='5'

##    imageID_A='A'
##    imageID_B='B'
##    imageID_C='C'
##    imageID_D='D'
##    imageID_E='E'
##    imageID_1='1'
##    imageID_2='2'
##    imageID_3='3'
##    imageID_4='4'
##    imageID_5='5'
##    imageID_UA='UA'
##    imageID_DA='DA'
##    imageID_RA='RA'
##    imageID_LA='LA'
##    imageID_CIR='CIR'


    
    ret_UA_Lower =0.3104 
    ret_Arrow_Lower= 0.0073
    ret_circle_Lower= 0
    ret_1_Lower= 0.493
    ret_2_Lower= 0.5045
    ret_3_Lower= 0.29
    ret_4_Lower= 0.0055
    ret_5_Lower= 0.2974
    ret_A_Lower= 0.0735
    ret_B_Lower= 0.0104
    ret_C_Lower= 0.213
    ret_D_Lower= 0.0078
    ret_E_Lower= 0.2936
    
    ret_UA_Upper = 0.3663
    ret_Arrow_Upper= 0.13
    ret_circle_Upper= 0.0038
    ret_1_Upper= 0.97
    ret_2_Upper= 1.2988
    ret_3_Upper= 0.7
    ret_4_Upper= 0.1035
    ret_5_Upper= 0.6056
    ret_A_Upper= 0.4
    ret_B_Upper= 0.0917
    ret_C_Upper= 0.3171
    ret_D_Upper= 0.0316
    ret_E_Upper= 0.5806

    len_UA_Lower =7
    len_Arrow_Lower=7 
    len_circle_Lower=8
    len_1_Lower= 7
    len_2_Lower= 12
    len_3_Lower= 11
    len_4_Lower= 13
    len_5_Lower= 12
    len_A_Lower= 6
    len_B_Lower= 7
    len_C_Lower= 27
    len_D_Lower= 8
    len_E_Lower= 10

    len_UA_Upper = 18
    len_Arrow_Upper= 14
    len_circle_Upper= 8
    len_1_Upper= 23
    len_2_Upper= 18
    len_3_Upper= 15
    len_4_Upper= 21
    len_5_Upper= 14
    len_A_Upper= 11
    len_B_Upper= 15
    len_C_Upper= 30
    len_D_Upper= 11
    len_E_Upper= 12

    area_UA_Lower = 15000
    area_Arrow_Lower= 15000
    area_circle_Lower= 22184
    area_1_Lower= 7000
    area_2_Lower= 12404
    area_3_Lower= 9707
    area_4_Lower= 11309
    area_5_Lower= 12740
    area_A_Lower= 14160
    area_B_Lower= 21861
    area_C_Lower= 11971
    area_D_Lower= 20781
    area_E_Lower= 15689

    area_Arrow_Upper= 34329
    area_circle_Upper= 45111
    area_UA_Upper = 31271
    area_1_Upper= 15010
    area_2_Upper= 25177
    area_3_Upper= 20994
    area_4_Upper= 24598
    area_5_Upper= 12740
    area_A_Upper= 29277
    area_B_Upper= 21861
    area_C_Upper= 11971
    area_D_Upper= 43394
    area_E_Upper= 29879

    

    board=[]
    for x in range (15):
        board.append([])
        for y in range(20):
            board[x].append([])

    def boardweighting(self):
        boardweightage =[]
        for x in range (15):
            boardweightage.append([])
            for y in range(20):
                boardweightage[x].append(0)
        itsWeight = 1
        upDownLeftRightWeight = 0.5
        diagonalWeight = 0.1
        # print(boardweightage)
        for x in range (15):
            # print(self.board[x])
            for y in range (20):
                try:
                    boardweightage[x][y] +=len(self.board[x][y]) *itsWeight
                    
                except:
                    pass
                try:
                    boardweightage[x-1][y] +=len(self.board[x][y]) * upDownLeftRightWeight
                    
                except:
                    pass
                try:
                    boardweightage[x+1][y] +=len(self.board[x][y]) * upDownLeftRightWeight
                    
                except:
                    pass
                try:
                    boardweightage[x][y-1] +=len(self.board[x][y]) * upDownLeftRightWeight
                    
                except:
                    pass
                try:
                    boardweightage[x][y+1] +=len(self.board[x][y]) * upDownLeftRightWeight
                    
                except:
                    pass
                try:
                    boardweightage[x+1][y+1] +=len(self.board[x][y]) * diagonalWeight
                    
                except:
                    pass
                try:
                    boardweightage[x-1][y+1] +=len(self.board[x][y]) * diagonalWeight
                    
                except:
                    pass
                try:
                    boardweightage[x+1][y-1] +=len(self.board[x][y]) * diagonalWeight
                    
                except:
                    pass
                try:
                    boardweightage[x-1][y-1] +=len(self.board[x][y]) * diagonalWeight
                    
                except:
                    pass
##            print(boardweightage[x])
                
    # print(board)
    # print(len(board[14]))


    #red
    # print('enter open files')
    thresh = cv2.imread('images/A.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_A = contours[0]

    thresh = cv2.imread('images/3.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_3 = contours[0]

    thresh = cv2.imread('images/DA.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_DA = contours[0]

    # #blue
    thresh = cv2.imread('images/D.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_D = contours[0]

    thresh = cv2.imread('images/1.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_1 = contours[0]

    thresh = cv2.imread('images/LA.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_la = contours[0]

    # #yellow
    thresh = cv2.imread('images/E.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_E = contours[0]

    thresh = cv2.imread('images/5.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_5 = contours[0]

    thresh = cv2.imread('images/stop.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_circle = contours[0]

    # #green
    thresh = cv2.imread('images/B.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_B = contours[0]

    thresh = cv2.imread('images/2.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_2 = contours[0]

    thresh = cv2.imread('images/RA.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_RA = contours[0]

    # #white
    thresh = cv2.imread('images/C.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_C = contours[0]

    thresh = cv2.imread('images/4.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_4 = contours[0]

    thresh = cv2.imread('images/UA.PNG', -1)
    (_, contours, _) = cv2.findContours(thresh, 2, 1)
    cnt_UA = contours[0]

    #red
##    thresh = cv2.imread('images/A.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_A = contours[0]
##
##    thresh = cv2.imread('images/3.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_3 = contours[0]
##
##    thresh = cv2.imread('images/DA.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_DA = contours[0]
##
##    #blue
##    thresh = cv2.imread('images/D.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_D = contours[0]
##
##    thresh = cv2.imread('images/1.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_1 = contours[0]
##
##    thresh = cv2.imread('images/LA.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_la = contours[0]
##
##    #yellow
##    thresh = cv2.imread('images/E.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_E = contours[0]
##
##    thresh = cv2.imread('images/5.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_5 = contours[0]
##
##    thresh = cv2.imread('images/stop.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_circle = contours[0]
##
##    #green
##    thresh = cv2.imread('images/B.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_B = contours[0]
##
##    thresh = cv2.imread('images/2.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_2 = contours[0]
##
##    thresh = cv2.imread('images/RA.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_RA = contours[0]
##
##    #white
##    thresh = cv2.imread('images/C.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_C = contours[0]
##
##    thresh = cv2.imread('images/4.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_4 = contours[0]
##
##    thresh = cv2.imread('images/UA.PNG', -1)
##    (contours, _) = cv2.findContours(thresh, 2, 1)
##    cnt_UA = contours[0]

    lower_red = np.array([0,160,0])
    upper_red = np.array([35,255,255])

    # blue color
    lower_blue = np.array([80, 65,65])
    upper_blue = np.array([120,235,200])

    # yellow color
    lower_yellow = np.array([5,165,50])
    upper_yellow = np.array([70,255,235])
    # lower_yellow = np.array([5,165,100])
    # upper_yellow = np.array([70,255,235])

    # green color
    lower_green = np.array([40,125,40])
    upper_green = np.array([85,255,220])
    # lower_green = np.array([20,100,90])
    # upper_green = np.array([110,200,210])

    
    results =[]
    def process_board(self):
        coordResults=[]
        for result in self.results:
            cX=result[2]
            cY=result[3]
            hX=result[4]
            hY=result[5]
            offset = result[6]
            if(cX==hX):               # x-axis same
                if(cY-hY == -1):
                    face = 'n'
                elif(cY-hY == 1):
                    face = 's'
            elif(cY==hY):           # y-axis same
                if(cX-hX== -1):
                    face = 'e'
                elif(cX-hX== 1):   
                    face = 'w'
            if(face =='n'):
                obsX = cX-2
                obsY = cY+offset
            if(face =='s'):
                obsX = cX+2
                obsY = cY-offset
            if(face =='e'):
                obsX = cX+offset
                obsY = cY+2
            if(face =='w'):
                obsX = cX-offset
                obsY = cY-2        
            coordResults.append([obsX,obsY,result[0],result[1]])
        print('coordresults: ',coordResults)
        
        
        if (coordResults):
            for coordResult in coordResults:
                x = coordResult[0]
                y = coordResult[1]
                id = coordResult[2]
                ret = coordResult[3]

                (self.board[x][y]).append([id,ret])
            self.boardweighting()
        # start of board Processing
        yellowList = []
        blueList = []
        greenList = []
        redList = []
        whiteList = []
        for x in range(15):
            for y in range(20):
                if self.board[x][y]:
                    # sort smallest to biggest
                    try:
                        self.board[x][y].sort(key = lambda x:x[1])
                    except:
                        pass

                try:
                    for possibleResult in self.board[x][y]:
                        if (possibleResult[0] in [self.imageID_CIR, self.imageID_5, self.imageID_E]):
                            yellowList.append(possibleResult)
                        elif (possibleResult[0] in [self.imageID_1,self.imageID_D,self.imageID_LA]):
                            blueList.append(possibleResult)    
                        elif (possibleResult[0] in [self.imageID_2,self.imageID_B,self.imageID_RA]):
                            greenList.append(possibleResult)    
                        elif (possibleResult[0] in [self.imageID_A,self.imageID_3,self.imageID_DA]):
                            redList.append(possibleResult)    
                        elif (possibleResult[0] in [self.imageID_UA,self.imageID_4,self.imageID_C]):
                            whiteList.append(possibleResult)
                    mostColor = max([len(blueList), len(yellowList), len(redList), len(greenList), len(whiteList)])
                    
                    if(mostColor > 0):
                        colourlst = []
                        if(len(yellowList) == mostColor):
                            colourlst.append(yellowList)
                        if(len(blueList) == mostColor):
                            colourlst.append(blueList)
                        if(len(redList) == mostColor):
                            colourlst.append(redList)
                        if(len(greenList) == mostColor):
                            colourlst.append(greenList)
                        if(len(whiteList) == mostColor):
                            colourlst.append(whiteList)
                    
                    if (len(colourlst) >1):
                        if (len(blueList)>0):
                            mini = blueList[0][1]
                            correctid =blueList[0][0]
                            for id in blueList:
                                if (id[1]<mini):
                                    mini = id[1]
                                    correctid = id[0]
                            self.board[x][y] = [correctid, len(self.board[x][y]), mini]
                        elif (len(whiteList)>0):
                            mini = whiteList[0][1]
                            correctid =whiteList[0][0]
                            for id in whiteList:
                                if (id[1]<mini):
                                    mini = id[1]
                                    correctid = id[0]
                            self.board[x][y] = [correctid, len(self.board[x][y]), mini]
                        elif (len(yellowList)>0):
                            mini = yellowList[0][1]
                            correctid =yellowList[0][0]
                            for id in yellowList:
                                if (id[1]<mini):
                                    mini = id[1]
                                    correctid = id[0]
                            self.board[x][y] = [correctid, len(self.board[x][y]), mini]
                        elif (len(redList)>len(greenList)>0):
                            mini = greenList[0][1]
                            correctid =greenList[0][0]
                            for id in greenList:
                                if (id[1]<mini):
                                    mini = id[1]
                                    correctid = id[0]
                            self.board[x][y] = [correctid, len(self.board[x][y]), mini]
                        elif (len(redList)>0):
                            mini = redList[0][1]
                            correctid =redList[0][0]
                            for id in redList:
                                if (id[1]<mini):
                                    mini = id[1]
                                    correctid = id[0]
                            self.board[x][y] = [correctid, len(self.board[x][y]), mini]
                    else:
                        mini = colourlst[0][0][1]
                        correctid =colourlst[0][0][0]
                        for id in colourlst[0]:
                            if (id[1]<mini):
                                mini = id[1]
                                correctid = id[0]
                        self.board[x][y] = [correctid, len(self.board[x][y]), mini]
                    yellowList = []
                    blueList = []
                    greenList = []
                    redList = []
                    whiteList = []
                    colourlst = []
                except:
                    pass
        photos = 0
        finalResults = []
        for x in range (15):
            for y in range (20):
                try:
                    if isinstance(self.board[x][y][0], str):
                        finalResults.append([x,y,self.board[x][y][0],self.board[x][y][1],self.board[x][y][2]])
                        photos+=1
                except:
                    pass
                
        sendingResult = finalResults
        limit = 5
        if(len(sendingResult)>limit):
            heapNumImage = []
            heapRET = []
            sendingResult = []
            sameLengthRET = []
            for finalResult in (finalResults[:(limit)]):
                heaps.heappush(heapRET, (-finalResult[4]))
                heaps.heappush(heapNumImage,finalResult[3])
                sendingResult.append(finalResult)
            for finalResult in (finalResults[limit:]):
                if(finalResult[3] >= heapNumImage[0]):
                    sendingResult.append(finalResult)
                    remove = heapNumImage[0]
                    lowestSameRET = []
                    for sameResult in sendingResult:
                        if(sameResult[3] == heapNumImage[0]):
                            sameLengthRET.append(sameResult[4])
                    lowestSameRET = max(sameLengthRET)
                    for x in  range(len(sendingResult)):
                        try:
                            if(sendingResult[x][4] == lowestSameRET):
                                del sendingResult[x]
                        except:
                            pass
                    heapNumImage = []
                    heapRET = []
                    sameLengthRET = []
                    for sendResult in sendingResult:
                        heaps.heappush(heapRET,sendResult[4])
                        heaps.heappush(heapNumImage,sendResult[3])
        print(sendingResult)

                    
        imageCoor = ''
        for result in sendingResult:
            imageCoor += '(' + str(result [0])+', '+str(result[1])+', '+str(result[2])+'),'
        imageCoor = imageCoor[:-1]

        jsonstr = '{"arrows": "'+imageCoor+'"}'
        print(jsonstr)
        return jsonstr

    def process_img(self, iptImg, iptName):
        if(iptName == 'END'):
            return self.process_board()
        
    
##    def process_img(self, iptName):
        # print(iptImg)
##        iptImg == input image
##        iptName == input JSON name format
        
        
        
        ##    receive array from Charlene
##        image = cv2.imread('7raw.jpg')
        
        image = iptImg
        # print(image)
        # cv2.imshow('iptImg', iptImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
##        image = cv2.cvtColor(iptImg, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (1088,480))
        # image = cv2.resize(image, (480,480))
        _,width,_ = image.shape
        # _, width,_ = iptImg.shape
        widthDivide1 = int(width/6)
        widthDivide2 = int(width*7/12)
        blur = cv2.medianBlur(image,5)
        # blur = image
        # cv2.imshow('image',image)
        # cv2.imshow('blur',blur)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # blur = image
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        first, second,third = iptName.split('(')
        centerCoor,_ = second.split(')')
        cX, cY = centerCoor.split(',')
        cX =int(cX)
        cY =int(cY)
        headCoor,_ = third.split(')')
        hX, hY = headCoor.split(',')
        hX = int(hX)
        hY = int(hY)

        

        # color masking
        print('enter masking')
        red_mask = cv2.inRange(hsv, self.lower_red, self.upper_red)
        kernel = np.ones((5, 5),"uint8")# np.uint8)

        red = cv2.dilate(red_mask, kernel)
        res = cv2.bitwise_and(image, image, mask=red)
        redGry = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        _, red_mask = cv2.threshold(redGry, 25, 255, 3)
        _, red_mask = cv2.threshold(red_mask, 255, 255, 4)
        # cv2.imshow('red',red_mask)
        # cv2.waitKey(0)
        
        # cv2.imshow('res', res)



        _, blue_mask = cv2.threshold(hsv, 25, 255, 3)
        _, blue_mask = cv2.threshold(blue_mask, 225, 255, 4)
        # _, blue_mask = cv2.threshold(blue_mask, 0, 255, 0)

        blue_mask = cv2.inRange(blue_mask, self.lower_blue, self.upper_blue)
        # cv2.imshow('gm1',blue_mask)


        yellow_mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        yellow = cv2.dilate(yellow_mask, kernel)
        res2 = cv2.bitwise_and(image, image, mask=red)
        yellowGry = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
        _, yellowGry = cv2.threshold(yellowGry, 25, 255, 3)
        _, yellowGry = cv2.threshold(yellowGry, 255, 255, 4)


        _, green_mask = cv2.threshold(hsv, 0, 255, 3)
        # cv2.imshow('gm1',green_mask)
        _, green_mask = cv2.threshold(green_mask, 255, 255, 4)
        # cv2.imshow('gm2',green_mask)
        green_mask = cv2.inRange(green_mask, self.lower_green, self.upper_green)

        # white masking
        whiteGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit= 0.00000001, tileGridSize=(2,2))
        whiteGrey = cv2.resize(whiteGrey,(272,120))
        # cv2.imshow('zero',whiteGrey)
        cl_img = clahe.apply(whiteGrey)
        testingWhite, whiteimagetest = cv2.threshold(cl_img, 50, 255, 3)
        # cv2.imshow('first', whiteimagetest)
        testingWhite, whiteimagetest = cv2.threshold(whiteimagetest, 200, 255, 4)
        # cv2.imshow('second', whiteimagetest)
        testingWhite, whiteimagetest = cv2.threshold(whiteimagetest, 0, 255, 0)
        # cv2.imshow('third', whiteimagetest)


        
        kernel = np.ones((5, 5),"uint8")
        
        red = cv2.dilate(red_mask, kernel)
        blue = cv2.dilate(blue_mask, kernel)
        yellow = cv2.dilate(yellow_mask, kernel)
        green = cv2.dilate(green_mask, kernel)
        white = cv2.dilate(whiteimagetest, kernel)

        # cv2.imshow('red',yellow)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # red
        
        print('enter red')
        (_, contours, hierarchy) = cv2.findContours(red, 2,1)
##        (contours, hierarchy) = cv2.findContours(red, 2,1)
        redlist0 = []
        redlist1 = []
        redlist2 = []
        for pic, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if (True):
                approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
                x, y, w, h = cv2.boundingRect(cnt)
##                print(w, h)
                ret_A = cv2.matchShapes(self.cnt_A,cnt, 1, 0)
                ret_DA = cv2.matchShapes(self.cnt_DA,cnt, 1, 0)
                ret_3 = cv2.matchShapes(self.cnt_3,cnt, 1, 0)
##                print('  ret_A: ', ret_A)
##                print('  ret_3: ', ret_3)
##                print(' ret_DA: ', ret_DA)
                if (x< widthDivide1):
                    x=-1
                elif(x>widthDivide2):
                    x=1
                else:
                    x = 0


                if(self.ret_A_Lower < ret_A < self.ret_A_Upper and self.len_A_Lower <=len(approx) <= self.len_A_Upper and self.area_A_Lower < area < self.area_A_Upper):
                    try:
                        if (redlist0[1] > ret_A):
                            redlist0 = [self.imageID_A,round(ret_A,5), cX, cY, hX, hY, x]
                    except:
                        redlist0 = [self.imageID_A,round(ret_A,5), cX, cY, hX, hY, x]
                if(self.ret_Arrow_Lower < ret_DA < self.ret_Arrow_Upper and self.len_Arrow_Lower<= len(approx) <= self.len_Arrow_Upper and self.area_Arrow_Lower < area < self.area_Arrow_Upper):
                    try:
                        if (redlist1[1] > ret_DA):
                            redlist1 = [self.imageID_DA,round(ret_DA,5), cX, cY, hX, hY, x]
                    except:
                        redlist1 = [self.imageID_DA,round(ret_DA,5), cX, cY, hX, hY, x]
##                        print(ret_DA, len(approx), area)
                    # cv2.imshow('red'+filename, image)
                    # cv2.imshow('red2'+filename, red_mask)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                if(self.ret_3_Lower < ret_3 < self.ret_3_Upper and self.len_3_Lower<= len(approx) <= self.len_3_Upper and self.area_3_Lower < area < self.area_3_Upper):
                    try:
                        if (redlist2[1] > ret_3):
                            redlist2 = [self.imageID_3,round(ret_3,5), cX, cY, hX, hY, x]
                    except:
                        redlist2 = [self.imageID_3,round(ret_3,5), cX, cY, hX, hY, x]


        if(redlist0):
            self.results.append(redlist0)
        if(redlist1):
            self.results.append(redlist1)
        if(redlist2):
            self.results.append(redlist2)
        # print(self.results)

                 
        # blue
        bluelist0 = []
        bluelist1 = []
        bluelist2 = []
        print('enter blue')
        (_, contours, hierarchy) = cv2.findContours(blue, 2, 1)
        for pic, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            
            if (True):
                approx = cv2.approxPolyDP(cnt, 0.009*cv2.arcLength(cnt, True), True)
                x, y, w, h = cv2.boundingRect(cnt)   
                ret_D = cv2.matchShapes(self.cnt_D,cnt, 1, 0)
                ret_1 = cv2.matchShapes(self.cnt_1,cnt, 1, 0)
                ret_LA = cv2.matchShapes(self.cnt_la,cnt, 1, 0)
##                print('  ret_D: ', ret_D)
##                print('  ret_1: ', ret_1)
##                print(' ret_LA: ', ret_LA)
                # print(ret_1)
                if (x< widthDivide1):
                    x=-1
                elif(x>widthDivide2):
                    x=1
                else:
                    x = 0

                    
                if(self.ret_D_Lower<ret_D < self.ret_D_Upper and self.len_D_Lower <= len(approx) <= self.len_D_Upper and self.area_D_Lower < area < self.area_D_Upper):
                    try:
                        if (bluelist0[1] > ret_D):
                            bluelist0 = [self.imageID_D,round(ret_D,5), cX, cY, hX, hY, x]
                    except:
                        bluelist0 = [self.imageID_D,round(ret_A,5), cX, cY, hX, hY, x]
                if(self.ret_Arrow_Lower < ret_LA <self.ret_Arrow_Upper and self.len_Arrow_Lower<=len(approx) <=  self.len_Arrow_Upper and self.area_Arrow_Lower < area < self.area_Arrow_Upper):
                    try:
                        if (bluelist1[1] > ret_LA):
                            bluelist1 = [self.imageID_LA,round(ret_LA,5), cX, cY, hX, hY, x]
                    except:
                        bluelist1 = [self.imageID_LA,round(ret_LA,5), cX, cY, hX, hY, x]
                if(self.ret_1_Lower < ret_1 < self.ret_1_Upper and self.len_1_Lower <= len(approx) <=self.len_1_Upper and self.area_1_Lower < area < self.area_1_Upper):
                    try:
                        if (bluelist2[1] > ret_1):
                            bluelist2 = [self.imageID_1,round(ret_1,5), cX, cY, hX, hY, x]
                    except:
                        bluelist2 = [self.imageID_1,round(ret_1,5), cX, cY, hX, hY, x]

        if(bluelist0):
            self.results.append(bluelist0)
        if(bluelist1):
            self.results.append(bluelist1)
        if(bluelist2):
            self.results.append(bluelist2)

                
                
        # yellow
        yellowlist0 =[]
        yellowlist1 =[]
        yellowlist2 =[]

        print('enter yellow')
        (_, contours, hierarchy) = cv2.findContours(yellow, 2,1)
##        (contours, hierarchy) = cv2.findContours(yellow, 2,1)
        for pic, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if (True):
                approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
                
                x, y, w, h = cv2.boundingRect(cnt)
                ret_E = cv2.matchShapes(self.cnt_E,cnt, 1, 0)
                ret_5 = cv2.matchShapes(self.cnt_5,cnt, 1, 0)
                ret_circle = cv2.matchShapes(self.cnt_circle,cnt, 1, 0)
##                print('  ret_E: ', ret_E)
##                print('  ret_5: ', ret_5)
##                print('ret_CIR: ', ret_circle)
                if (x< widthDivide1):
                    x=-1
                elif(x>widthDivide2):
                    x=1
                else:
                    x = 0
                
                
                if(self.ret_E_Lower < ret_E < self.ret_E_Upper and self.len_E_Lower <= len(approx) <= self.len_E_Upper and self.area_E_Lower < area < self.area_E_Upper):
                    try:
                        if (yellowlist0[1] > ret_E):
                            yellowlist0 = [self.imageID_E,round(ret_E,5), cX, cY, hX, hY, x]
                    except:
                        yellowlist0 = [self.imageID_E,round(ret_E,5), cX, cY, hX, hY, x]
                if(self.ret_5_Lower < ret_5 < self.ret_5_Upper and self.len_5_Lower <= len(approx) <= self.len_5_Upper and self.area_5_Lower < area < self.area_5_Upper):
                    try:
                        if (yellowlist1[1] > ret_5):
                            yellowlist1 = [self.imageID_5,round(ret_5,5), cX, cY, hX, hY, x]
                    except:
                        yellowlist1 = [self.imageID_5,round(ret_5,5), cX, cY, hX, hY, x]
                if(self.ret_circle_Lower< ret_circle < self.ret_circle_Upper and self.len_circle_Lower <= len(approx) <= self.len_circle_Upper and self.area_circle_Lower < area < self.area_circle_Upper):
                    try:
                        if (yellowlist2[1] > ret_circle):
                            yellowlist2 = [self.imageID_CIR,round(ret_circle,5), cX, cY, hX, hY, x]
                    except:
                        yellowlist2 = [self.imageID_CIR,round(ret_circle,5), cX, cY, hX, hY, x]

        if(yellowlist0):
            self.results.append(yellowlist0)
        if(yellowlist1):
            self.results.append(yellowlist1)
        if(yellowlist2):
            self.results.append(yellowlist2)
                
        # green
        greenlist0 = []
        greenlist1 = []
        greenlist2 = []
        
        print('enter green')
        (_,contours, hierarchy) = cv2.findContours(green, 2,1)
        for pic, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if (True):
                approx = cv2.approxPolyDP(cnt, 0.009*cv2.arcLength(cnt, True), True)

                x, y, w, h = cv2.boundingRect(cnt)
                ret_B = cv2.matchShapes(self.cnt_B,cnt, 1, 0)
                ret_2 = cv2.matchShapes(self.cnt_2,cnt, 1, 0)
                ret_RA = cv2.matchShapes(self.cnt_RA,cnt, 1, 0)
##                print('  ret_B: ', ret_B)
##                print('  ret_2: ', ret_2)
##                print(' ret_RA: ', ret_RA)
                if (x< widthDivide1):
                    x=-1
                elif(x>widthDivide2):
                    x=1
                else:
                    x = 0

                
                if(self.ret_B_Lower < ret_B < self.ret_B_Upper and self.len_B_Lower <= len(approx) <=self.len_B_Upper and self.area_B_Lower < area < self.area_B_Upper):
                    try:
                        if (greenlist0[1] > ret_B):
                            greenlist0 = [self.imageID_B,round(ret_B,5), cX, cY, hX, hY, x]
                    except:
                        greenlist0 = [self.imageID_B,round(ret_B,5), cX, cY, hX, hY, x]

                if(self.ret_2_Lower < ret_2 < self.ret_2_Upper and self.len_2_Lower <= len(approx) <= self.len_2_Upper and self.area_2_Lower < area < self.area_2_Upper):
                    try:
                        if (greenlist1[1] > ret_circle):
                            greenlist1 = [self.imageID_2,round(ret_2,5), cX, cY, hX, hY, x]
                    except:
                        greenlist1 = [self.imageID_2,round(ret_2,5), cX, cY, hX, hY, x]

                if(self.ret_Arrow_Lower < ret_RA < self.ret_Arrow_Upper and self.len_Arrow_Lower <=len(approx) <=self.len_Arrow_Upper and self.area_Arrow_Lower < area < self.area_Arrow_Upper):
                    try:
                        if (greenlist2[1] > ret_circle):
                            greenlist2 = [self.imageID_RA,round(ret_RA,5), cX, cY, hX, hY, x]
                    except:
                        greenlist2 = [self.imageID_RA,round(ret_RA,5), cX, cY, hX, hY, x]

                
        if(greenlist0):
            self.results.append(greenlist0)
        if(greenlist1):
            self.results.append(greenlist1)
        if(greenlist2):
            self.results.append(greenlist2)
                
        # white
        whitelist0 = []
        whitelist1 = []
        whitelist2 = []

        print('enter white')
        (_,contours, hierarchy) = cv2.findContours(white, 2,1)
        for pic, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if (True):
                approx = cv2.approxPolyDP(cnt, 0.004*cv2.arcLength(cnt, True), True)

                x, y, w, h = cv2.boundingRect(cnt)
                ret_C = cv2.matchShapes(self.cnt_C,cnt, 1, 0)
                ret_4 = cv2.matchShapes(self.cnt_4,cnt, 1, 0)
                ret_UA = cv2.matchShapes(self.cnt_UA,cnt, 1, 0)
##                print('  ret_C: ', ret_C)
##                print('  ret_4: ', ret_4)
##                print(' ret_UA: ', ret_UA)
                if (x< widthDivide1):
                    x=-1
                elif(x>widthDivide2):
                    x=1
                else:
                    x = 0

                if(self.ret_C_Lower < ret_C < self.ret_C_Upper and self.len_C_Lower <= len(approx) <= self.len_C_Upper and self.area_C_Lower < area < self.area_C_Upper):
                    try:
                        if (greenlist2[1] > ret_C):
                            greenlist2 = [self.imageID_C,round(ret_C,5), cX, cY, hX, hY, x]
                    except:
                        greenlist2 = [self.imageID_C,round(ret_C,5), cX, cY, hX, hY, x]
                if(self.ret_4_Lower < ret_4 < self.ret_4_Upper and self.len_4_Lower <= len(approx) <= self.len_4_Upper and self.area_4_Lower < area < self.area_4_Upper):
                    try:
                        if (greenlist2[1] > ret_4):
                            greenlist2 = [self.imageID_4,round(ret_4,5), cX, cY, hX, hY, x]
                    except:
                        greenlist2 = [self.imageID_4,round(ret_4,5), cX, cY, hX, hY, x]
                if(self.ret_Arrow_Lower < ret_UA < self.ret_Arrow_Upper and self.len_Arrow_Lower <= len(approx)<= self.len_Arrow_Upper and self.area_UA_Lower < area < self.area_UA_Upper):
                    try:
                        if (greenlist2[1] > ret_UA):
                            greenlist2 = [self.imageID_UA,round(ret_UA,5), cX, cY, hX, hY, x]
                    except:
                        greenlist2 = [self.imageID_UA,round(ret_UA,5), cX, cY, hX, hY, x]


        if(whitelist0):
            self.results.append(whitelist0)
        if(whitelist1):
            self.results.append(whitelist1)
        if(whitelist2):
            self.results.append(whitelist2)
        print('ended processing')
        print(self.results)

        # image = cv2.resize(image, (200,200))
        # yellow_mask = cv2.resize(yellow_mask, (200,200))
        # whiteimagetest = cv2.resize(whiteimagetest, (200,200))
        # red_mask = cv2.resize(red_mask, (200,200))
        # blue_mask = cv2.resize(blue_mask, (200,200))
        # green_mask = cv2.resize(green_mask, (200,200))
        # cv2.imshow('yellow', yellow_mask)
        # cv2.imshow('white', whiteimagetest)
        # cv2.imshow('red', red_mask)
        # cv2.imshow('blue', blue_mask)
        # cv2.imshow('green', green_mask)
        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if(abs(cX-self.x) >=2 or abs(cY-self.y) >=2):
            resultB4End =  self.process_board()
            self.x = cX
            self.y = cY

            board=[]
            for x in range (15):
                
                for y in range(20):
                    self.board[x][y]=[]

                   
            return resultB4End
        self.x = cX
        self.y = cY
        
        
        jsonstr = '{"arrows": ""}'
        print(jsonstr)
        return jsonstr 

##        cv2.imshow("image", image)
##        cv2.waitKey(0)
##        cv2.destroyAllWindows()
        


    
