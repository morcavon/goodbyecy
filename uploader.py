# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        uploader.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/04/29
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------


import os, re, httplib, time, wx

#import psyco
#psyco.full()
#psyco.profile(0.0)

from config import Config
from picture import Picture
from post import Post

from threading import Thread
import tools
import time


class Uploader(Thread):
    LIMIT_TISTORY = 500
    
    def __init__(self, parent):
        Thread.__init__(self)
        
        self.parent = parent
        self.config = parent.config
        self.downloader = parent.downloader
        
        self.currentUploadingFolder = ""
        self.postedCount = 0
        self.recentFolderName = ""
        
        self.isRunning = False
        
        
        
        
    def run(self):
        """ downloader의 pictureList에서 데이터를 가져와서 블로그에 포스팅 """
        
        self.isRunning = True
        
        uploadList = []         # 포스트 하나에 포함할 사진 게시물 리스트
        while True:
            
            if not self.isRunning:
                tools.stoppedByUser(self)
                return
            
            while self.isRunning and len(self.downloader.pictureList) == 0:
                if self.parent.debug:   print "uploader.run: wait for pictureList, current picureList length=", len(self.downloader.pictureList)
                time.sleep(0.5)
            
            try:
                picture = self.downloader.pictureList.pop(0)        # 큐에서 사진 하나를 가져옴
            except:
                continue
            
            
            # 포스팅 종료
            if picture == None:
                
                break
            
            
            
            
            # 카테고리가 바뀌면 업로드 시킴 (첫 게시물은 경우는 넘어감),
            # 카테고리가 바꼈단 얘기는 방금까지 진행했던 폴더의 포스팅이 완료되었다는 의미
            if len(uploadList) > 0 and uploadList[-1].category != picture.category:
                uploadList = self.upload(uploadList, True)
                self.logFinishedPage(uploadList[-1], 0)

            uploadList.append(picture)    
                
            
            # 포스트당 최대 게시물 만큼 모은 경우
            if self.config.maxItemCount == len(uploadList):
                uploadList = self.upload(uploadList)
                
        # end of while
        
        
        
        if len(uploadList) > 0:            # 남은것들....
            uploadList = self.upload(uploadList, True)
                        
      
        # 완료됐다는 표시
        if self.parent.debug: print "uploader.run: logging finish", self.recentFolderName
        self.logFinishedPage(self.recentFolderName, 0)
        
      
        self.isRunning = False
    


    def logFinishedPage(self, category, pageNo):
        """ 포스팅이 완료된 페이지 번호 기록 (결국 config에는 가장 최근에 작업중이었던 페이지 번호가 들어감, 완료된것이 아니라) """
        import math
        
        
        
        # 메인 화면의 폴더 리스트의 텍스트를 업데이트 함
        if pageNo != self.config.recentlyPageNo.get(category, -1):
            for idx, label in enumerate(self.parent.folderListChkListBox.GetItems()):
                if category in label:
                    folder = self.parent.folderList[idx]
                    self.parent.folderListChkListBox.SetString(idx, "%s (%s, %d/%d)" % (folder["name"], folder["count"], pageNo,int(math.ceil(int(folder["count"]) / 20.0))))
                    self.parent.folderListChkListBox.Refresh()
                    break
        
        
        
        self.config.recentlyPageNo[category] = pageNo
        
        return True




    
    def upload(self, uploadList, end=False):
        """ end가 True면 이번 리스트가 해당 폴더의 마지막 페이지라는 의미 """
        
        if len(uploadList) > 0:
            
            if self.parent.debug: print "uploader.upload.uploadList: ", uploadList
        
            post = Post(self.parent.server, uploadList, self.config, self.parent.blogPasswordTxt.GetValue(), self.parent.debug)
                    
            
            self.currentUploadingFolder = uploadList[0].filename
            self.recentFolderName = uploadList[0].category
            
            # 블로그에 업로드....
            result = post.upload(self.parent.debug) 
            
            
            
            
            # 포스팅 오류 처리
            if result == 5:      # TOO MANY POSTING fault
                dlg = wx.MessageDialog(self.parent, '해당 블로그의 하루 최대 포스팅 제한에 걸렸습니다. 내일 다시 시도해주세요ㅠㅠ\r\n(현재까지 포스팅 완료된 위치는 저장되어 다음번 실행시 이어서 작업 할 수 있습니다)', '오류', wx.OK | wx.ICON_ERROR)
                try:
                    result = dlg.ShowModal()
                finally:
                    dlg.Destroy()
                    tools.stoppedByUser(self, "블로그 하루 최대 포스팅 개수 제한에 의해 작업이 중단되었습니다.")
            
            
            if result == 101:   # Invalid Login, egloos
                dlg = wx.MessageDialog(self.parent, '블로그 접속에 문제가 있습니다. 블로그 API 정보를 확인하세요.', '오류', wx.OK | wx.ICON_ERROR)
                try:
                    result = dlg.ShowModal()
                finally:
                    dlg.Destroy()
                    tools.stoppedByUser(self, "블로그 접속 문제로 인해 작업이 중단되었습니다.")                    
                
            
            
        
            # 포스트 완료후 카운트 증가
            self.postedCount += len(uploadList)
        
        
        # 해당 페이지의 마지막 포스트인 경우에만 기록
        self.logFinishedPage(uploadList[-1].category, uploadList[-1].pageNo)
        
        return []
    
    
    
    
        
        
    def garbageCollector(self):
        pass
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    