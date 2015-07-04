# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        config.py
#
# Author:      Jae Young
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
#
# Created:     2008/12/04
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------


import cPickle, os

class Config:
    def __init__(self):
        self.blogAPI = {"address":"", "ID":"", "userID":""}
        
        self.maxItemCount = 4               # 최대 100개 (한 페이지)
        self.categoryName = "사진첩"
        self.viewPolicy = {"전체공개":"비공개", "비공개":"비공개", "일촌공개":"비공개"}
        self.getComments = True
        self.doSyncDate = False
        self.cyLogin = "싸이 로그인 이메일"
        self.version = ""
        self.recentlyPageNo = {}           # 폴더별 가장 최근에 포스팅이 완료된 페이지 번호
        
    
    @staticmethod
    def getConfig(version):
        try:
            retValue = None
            if not os.path.exists(os.getcwd() + "/config.dat"):
                retValue = Config()
                retValue.version = version
            else:
                retValue = cPickle.load(open(os.getcwd() + "/config.dat", "rb"))
                
                # 기존 config.dat 파일이 현재 프로그램이 사용하는것과 같은지 검사
                # 버전이 다르면 새로 하나 만들어....
                if retValue.version != version:
                    retValue = Config()
            
            return retValue
        
        except:
            return None
        
    @staticmethod
    def saveConfig(config):
        cPickle.dump(config, open(os.getcwd() + "/config.dat", "wb"), cPickle.HIGHEST_PROTOCOL)
        
        
    @staticmethod
    def checkNewVersion(version, debug = False):
        """ 업데이트 체크 """
        
        import urllib, re
        
        if debug:
            return False

        try:
            contents = urllib.urlopen("http://goodbyecy.appspot.com/version").read()
            newVersion = contents
        except Exception, msg:
            if debug:
                print "version reading error"
                print msg
            return False

        # 버전 넘버 체크 (x.x.xx)
        for idx, newNumber in enumerate(newVersion.split(".")):
            if debug:   print int(version.split(".")[idx]) , int(newNumber)
            if int(version.split(".")[idx]) < int(newNumber):
                return True
            elif int(version.split(".")[idx]) > int(newNumber):
                return False
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    