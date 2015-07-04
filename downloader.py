# -*- coding: mbcs -*-
#-----------------------------------------------------------------------------
# Name:        downloader.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/27
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------

import os, re, httplib, time
import sys, traceback

#import psyco
#psyco.full()
#psyco.profile(0.0)

import wx

from config import Config
from picture import Picture
from threading import Thread
import tools
import time
import urllib
from cookcook import CookCook


class Downloader(Thread):
    """ 사진첩에서 사진을 다운 받는 쓰레드..."""
    """ 여기서는 사용자에게 로깅을 해주지 않음..."""
    
    MAX_QUEUE_SIZE = 50                 # pictureList에 저장할 최대 사진 개수
    
    def __init__(self, parent, down2pc=False):  
        import string
              
        Thread.__init__(self)
        self.parent = parent
        self.config = parent.config
        self.down2pc = down2pc
        self.targetDir = parent.targetDir
        
        self.pictureList = []
        
        
        self.logFile = open("goodbyeCy.log", "a")
        self.downloadedCount = 0        # 포스팅까지 처리완료된 갯수
        self.currentFolder = ""            # 현재 작업중인 사진첩 폴더의 이름
        
        s1="""\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
        s2="""_________________________________!^#$%&!'()$+,-_@0123456789#;&=~%@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{`}~"""
        self.pathNameTransTable = string.maketrans(s1, s2)

        
        self.folderList = []
        # 리스트 박스에서 체크한 폴더만 추려냄
        for idx in range(len(parent.folderList)):
            if parent.folderListChkListBox.IsChecked(idx):
                self.folderList.append(parent.folderList[idx])
        
        self.totalPictureCount = Picture.getTotalCount(self.folderList)
        
        self.isRunning = False
    
    
    def run(self):
        
        self.isRunning = True
        
        self.pictureList = []
        
        if self.parent.debug:  print "downloader.run: before getPicture()"
        
        for picture in self.getPicture():
            
            self.currentFolder = picture.filename
            
            
            # 최대 큐 사이즈만큼 저장되 있으면 1초 동안 기다렸다가 다시 시도...
            if not self.down2pc:
                while len(self.pictureList) >= Downloader.MAX_QUEUE_SIZE:
                    if self.parent.debug:  print "downloader.run: pending for max queue size"
                    time.sleep(2)
            
                self.pictureList.append(picture)            # 큐의 마지막에 추가....
                
            else:
                # 포스팅하지 않고 바로 pc에 다운받는 경우....
                self.saveImage2Local(picture)
            

        self.pictureList.append(None)           # termination
        
        if self.parent.debug:  
            print "@@@@@ downloader end...."
        
            
        # 종료 처리
        self.isRunning = False
        self.parent.isRunning = False
   
    
    
    
    def saveImage2Local(self, picture):
        import os
        from datetime import datetime
        picture.category = self.pathNameCheck(picture.category)
        path = os.path.join(self.targetDir.encode("mbcs"), "미니홈피 사진첩", picture.category)
        fullpath = os.path.join(path, datetime.strftime(picture.createTime, "%Y%m%d%H%M") + "_" + picture.filename)

        
        if not os.path.exists(path):
            os.makedirs(path)
        
        
        try:
            # preview...
            open(fullpath, "wb").write(picture.data)
            
            if self.parent.previewCheckBox.GetValue() and not fullpath.endswith("swf"):
                img = wx.Image(fullpath)
                bmp = None
                try:
                    img.Rescale(self.parent.previewBitmap.GetClientSize().x, self.parent.previewBitmap.GetClientSize().y)
                    bmp = img.ConvertToBitmap()
                    self.parent.previewBitmap.SetBitmap(bmp)
                except:
                    pass
            
        except:
            if self.parent.debug:
                traceback.print_exc(file=sys.stdout)
            print >> self.logFile, """[사진 저장 실패]
폴더명: %s
파일명: %s

                        
""" % (picttegory, picture.filename)    
        
    
    
    
    
    def garbageCollector(self):
        """ 임시 파일 정리 """
        pass
    
    
    
    def getPicture(self):
        """ 게시물 하나를 읽어와서 Picture 객체 리턴... """
        
        import math
        
        imgRex = """view_detail_thumbnail\('\d+', (\d+).+?<img src='(.+?)' border"""
        pageUrl = """/pims/board/image/imgbrd_list_thumbnail.asp?tid=%s&board_no=%s&search_content=&search_type=&search_keyword=&cpage=%d&AllCnt=0&board_nm=%s"""
        imgUrl =  """/pims/board/image/imgbrd_view_thumbnail.asp?tid=%s&item_seq=%s&board_no=%s&cpage=%d&list_type=&search_type=&search_keyword=&search_content=&cpage_original="""
        
        
#        if self.parent.debug:
#            print "downloader.getPicture().forlder list ", self.folderList

        
        for folder in self.folderList:
            
            
            ##################### 마지막 페이지부터 작업 #################################
            recentPageNo = self.config.recentlyPageNo.get(folder["name"], -1)
            
            #===================================================================
            # pc 다운시에는 이어받기 지원이 안됨...
            if recentPageNo == -1 or self.down2pc == True:
               startPageNo = int(math.ceil(int(folder["count"]) / 20.0))
            else:
                startPageNo = recentPageNo
            #===================================================================
            
            for pageNo in range(startPageNo, 0, -1):
                url = pageUrl % (self.parent.pimid, folder["seq"], pageNo, folder["board_nm"])
                temp = self.parent.mycook.getPage(url, cookie_select=self.parent.mycook.cookie_photo, host="minihp.cyworld.com",
                                     language="ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4", charset="windows-949,utf-8;q=0.7,*;q=0.3",
                                     accept="application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
                if self.parent.debug:   open("사진첩페이지로딩후.html", "w").write(temp)
                pageContent = temp
                
                # 페이지 하나에서 item_seqs, item_urls 뽑아내기
                sequencePairs = re.compile(imgRex).findall(pageContent)        
                
#                if self.parent.debug:
#                    print "downloader.getPicture: sequencePairs", sequencePairs
#                    print "Page %d, total %d images" % (pageNo, len(sequencePairs))        
                
                
                # 오래된 게시물부터 가져오기 위해 리스트를 뒤집음
                sequencePairs.reverse()
                
                for item_seq, item_url in sequencePairs:     
                    if not self.isRunning:
                        tools.stoppedByUser(self)
                        return
                    
                    url = imgUrl % (self.parent.pimid, item_seq, folder["seq"], pageNo)
                    temp = self.parent.mycook.getPage(url, cookie_select=self.parent.mycook.cookie_photo, host="minihp.cyworld.com",
                                     language="ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4", charset="windows-949,utf-8;q=0.7,*;q=0.3",
                                     accept="application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
                    if self.parent.debug:   open("각이미지페이지로딩후.html", "w").write(temp)

                    imgContents = temp
                    
                    if self.parent.debug:
                        print >> self.logFile, "downloader.getPicture.:tempURL=", url
                    
                    if imgContents == None:     # 페이지 로딩에 문제가 있을 경우 그냥 무시하고 다음으로 넘어감
                        if self.parent.debug:
                            print "downloader.getPicture: error while getSinglePage"
                            
                        print >> self.logFile, """[게시물 데이터 다운로드 실패]
폴더명: %s
페이지 번호: %d
URL: %s

                        
""" % (folder["name"], pageNo, url)                        

                        continue
                    
                    
                    if self.parent.debug:   open("before_getInstance.html", "w").write(imgContents)
                    
                    retValue = Picture.getInstance(imgContents, self.config.doSyncDate, self.config.getComments, folder["name"], pageNo)
                    temp = self.getImageContent(item_url)
                    
                    if temp == None:
                        if self.parent.debug:
                            print "downloader.getPicture: error while getImageContent"
                            

                        print >> self.logFile, """[이미지 파일 다운로드 실패]
폴더명: %s
제목: %s
파일명: %s
관련URL: %s
                       
""" % (retValue.category, retValue.title, retValue.filename, url)

                            
                        continue
                    
                    retValue.data = temp["content"]
                    retValue.filename = temp["name"]
                    
                    self.downloadedCount += 1
                    
                    yield retValue
                    
                    time.sleep(0.3)
        
        
        if self.parent.debug:    print "@@@@@@@@@@@ getpicture reuturn"
        
        return
    
    
    
      
    
    
    
    def getImageContent(self, imgUrl, saveDir=os.getcwd(), fname_prefix = ""):
        """ image 하나를 받아와서 리턴. """
        
        if self.parent.debug:   print "getImageContent.imgUrl=", imgUrl
        
        # swf url 처리....
        imgUrl = imgUrl.replace("file_down_swf.asp", "file_down_profile.asp")

        try:
            host = re.search("http://(cy.+?)/", imgUrl).group(1)
            getUrl = re.search("(/common/.+)", imgUrl).group(1)
            
#            if self.parent.debug:   print "host: %s, url: %s" % (host, getUrl)

#            host="cyimg.cyworld.com"
            h = httplib.HTTPConnection(host)
            h.putrequest("GET", getUrl, skip_accept_encoding=True, skip_host=True)

            h.putheader('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            h.putheader("Accept-Language", "ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4")
            h.putheader("Accept-Encoding", "gzip,deflate,sdch")
            h.putheader("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322)")
            h.putheader("Host", host)
            h.putheader("Connection", "Keep-Alive")
            h.putheader("Cache-Control", "max-age=0")
            h.putheader("Cookie", self.parent.mycook.cookie_photo)

            h.endheaders()
            
            response = h.getresponse()
#            if self.parent.debug:   print response.getheaders()
            
            dataLength = None
            for el in response.getheaders():
                if self.parent.debug:   print "downloader.getImageCotent: getheaders", el
                if el[0] == "content-length":
                    dataLength = int(el[1])
                
                elif el[0] == "content-disposition":
                    filename = el[1].split("filename=")[1].split(",")[0]

                    
            
            
            data = response.read(dataLength)
            
#            if self.parent.debug and dataLength <= 300:   
#               open("temp", "w").write(data)
            

            return {"name": filename, "content":data}



        except Exception, v:
            if self.parent.debug:
                print "@saveImage error: ", imgUrl, v
                traceback.print_exc(file=sys.stdout)
            return None

        


    def pathNameCheck(self, pname):
        """ 윈도우의 폴더명에 적합하지 않은 문자들을 대체하여 리턴 """
        return pname.translate(self.pathNameTransTable)

