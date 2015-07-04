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
        """ downloader�� pictureList���� �����͸� �����ͼ� ��α׿� ������ """
        
        self.isRunning = True
        
        uploadList = []         # ����Ʈ �ϳ��� ������ ���� �Խù� ����Ʈ
        while True:
            
            if not self.isRunning:
                tools.stoppedByUser(self)
                return
            
            while self.isRunning and len(self.downloader.pictureList) == 0:
                if self.parent.debug:   print "uploader.run: wait for pictureList, current picureList length=", len(self.downloader.pictureList)
                time.sleep(0.5)
            
            try:
                picture = self.downloader.pictureList.pop(0)        # ť���� ���� �ϳ��� ������
            except:
                continue
            
            
            # ������ ����
            if picture == None:
                
                break
            
            
            
            
            # ī�װ��� �ٲ�� ���ε� ��Ŵ (ù �Խù��� ���� �Ѿ),
            # ī�װ��� �ٲ��� ���� ��ݱ��� �����ߴ� ������ �������� �Ϸ�Ǿ��ٴ� �ǹ�
            if len(uploadList) > 0 and uploadList[-1].category != picture.category:
                uploadList = self.upload(uploadList, True)
                self.logFinishedPage(uploadList[-1], 0)

            uploadList.append(picture)    
                
            
            # ����Ʈ�� �ִ� �Խù� ��ŭ ���� ���
            if self.config.maxItemCount == len(uploadList):
                uploadList = self.upload(uploadList)
                
        # end of while
        
        
        
        if len(uploadList) > 0:            # �����͵�....
            uploadList = self.upload(uploadList, True)
                        
      
        # �Ϸ�ƴٴ� ǥ��
        if self.parent.debug: print "uploader.run: logging finish", self.recentFolderName
        self.logFinishedPage(self.recentFolderName, 0)
        
      
        self.isRunning = False
    


    def logFinishedPage(self, category, pageNo):
        """ �������� �Ϸ�� ������ ��ȣ ��� (�ᱹ config���� ���� �ֱٿ� �۾����̾��� ������ ��ȣ�� ��, �Ϸ�Ȱ��� �ƴ϶�) """
        import math
        
        
        
        # ���� ȭ���� ���� ����Ʈ�� �ؽ�Ʈ�� ������Ʈ ��
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
        """ end�� True�� �̹� ����Ʈ�� �ش� ������ ������ ��������� �ǹ� """
        
        if len(uploadList) > 0:
            
            if self.parent.debug: print "uploader.upload.uploadList: ", uploadList
        
            post = Post(self.parent.server, uploadList, self.config, self.parent.blogPasswordTxt.GetValue(), self.parent.debug)
                    
            
            self.currentUploadingFolder = uploadList[0].filename
            self.recentFolderName = uploadList[0].category
            
            # ��α׿� ���ε�....
            result = post.upload(self.parent.debug) 
            
            
            
            
            # ������ ���� ó��
            if result == 5:      # TOO MANY POSTING fault
                dlg = wx.MessageDialog(self.parent, '�ش� ��α��� �Ϸ� �ִ� ������ ���ѿ� �ɷȽ��ϴ�. ���� �ٽ� �õ����ּ���Ф�\r\n(������� ������ �Ϸ�� ��ġ�� ����Ǿ� ������ ����� �̾ �۾� �� �� �ֽ��ϴ�)', '����', wx.OK | wx.ICON_ERROR)
                try:
                    result = dlg.ShowModal()
                finally:
                    dlg.Destroy()
                    tools.stoppedByUser(self, "��α� �Ϸ� �ִ� ������ ���� ���ѿ� ���� �۾��� �ߴܵǾ����ϴ�.")
            
            
            if result == 101:   # Invalid Login, egloos
                dlg = wx.MessageDialog(self.parent, '��α� ���ӿ� ������ �ֽ��ϴ�. ��α� API ������ Ȯ���ϼ���.', '����', wx.OK | wx.ICON_ERROR)
                try:
                    result = dlg.ShowModal()
                finally:
                    dlg.Destroy()
                    tools.stoppedByUser(self, "��α� ���� ������ ���� �۾��� �ߴܵǾ����ϴ�.")                    
                
            
            
        
            # ����Ʈ �Ϸ��� ī��Ʈ ����
            self.postedCount += len(uploadList)
        
        
        # �ش� �������� ������ ����Ʈ�� ��쿡�� ���
        self.logFinishedPage(uploadList[-1].category, uploadList[-1].pageNo)
        
        return []
    
    
    
    
        
        
    def garbageCollector(self):
        pass
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    