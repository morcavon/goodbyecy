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
        
        self.maxItemCount = 4               # �ִ� 100�� (�� ������)
        self.categoryName = "����ø"
        self.viewPolicy = {"��ü����":"�����", "�����":"�����", "���̰���":"�����"}
        self.getComments = True
        self.doSyncDate = False
        self.cyLogin = "���� �α��� �̸���"
        self.version = ""
        self.recentlyPageNo = {}           # ������ ���� �ֱٿ� �������� �Ϸ�� ������ ��ȣ
        
    
    @staticmethod
    def getConfig(version):
        try:
            retValue = None
            if not os.path.exists(os.getcwd() + "/config.dat"):
                retValue = Config()
                retValue.version = version
            else:
                retValue = cPickle.load(open(os.getcwd() + "/config.dat", "rb"))
                
                # ���� config.dat ������ ���� ���α׷��� ����ϴ°Ͱ� ������ �˻�
                # ������ �ٸ��� ���� �ϳ� �����....
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
        """ ������Ʈ üũ """
        
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

        # ���� �ѹ� üũ (x.x.xx)
        for idx, newNumber in enumerate(newVersion.split(".")):
            if debug:   print int(version.split(".")[idx]) , int(newNumber)
            if int(version.split(".")[idx]) < int(newNumber):
                return True
            elif int(version.split(".")[idx]) > int(newNumber):
                return False
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    