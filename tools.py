# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        tools.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/29
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------

import wx

import re, sys, traceback, time
from config import Config
from cookcook import CookCook



def login(self):
    """ ���̿� �α����� �ϰ� �̴�Ȩ�� ����ø�� ���� ����Ʈ�� ����"""
    import os

    self.mainStatusBar.SetLabel("�α��� �� ����ø ���� �������� ��....(10�� ���� �ҿ�)")

    self.mycook = CookCook(self.cyLoginEmailTxt.GetValue(), self.cyLoginPasswordTxt.GetValue(), self.debug)
    
    while True:
        self.mycook.getCookie()
    
        if self.mycook.errmsg != "":
            # �α��� ����
            self.mainStatusBar.SetLabel(self.mycook.errmsg)
            return False
    
        else:
            #=======================================================================
            # ����ø �Խ��� ������ ��������...
            #=======================================================================
            
            
            self.pimid = self.mycook.tid
            
            url = """/svcs/MiniHp.cy/index/%s?tid=%s&urlstr=phot""" % (self.pimid, self.pimid)
            if self.debug: print url
    
            result = self.mycook.getPage(url, cookie_select=self.mycook.cookie_photo, host="minihp.cyworld.com",
                                         language="ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4", charset="windows-949,utf-8;q=0.7,*;q=0.3",
                                         accept="application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
    
            if self.debug:
                open("after_login_����ø�Խ��Ƿε���.html", "w").write(result)
    
            if "<h1>Bad Request</h1>" not in result:
                break
            else:
                if self.debug:  print "tool.login: ����ø �Խ��� �ε� ����"
    
    
    
    #=======================================================================
    # # ���� ����Ʈ ��������
    #=======================================================================
    folderList = []
    paramTemplate = """id="(foldernm.+?)".+?InframeNavi\('(\d+).+?'\).+?>(.+?)</a>"""
    param = re.compile(paramTemplate, re.DOTALL).findall(result)


    try:
        for board_nm, seq, real_nm in param:

            real_nm = real_nm.replace("""<img src='http://c1img.cyworld.co.kr/img/ico/new.gif' width=9 height=9 border=0/>""", "").strip()


            # ��ü���� ����
            if real_nm == "��ü����":
                continue


            # ������ �Խ��� ���� ��������...
            url = """/pims/board/image/imgbrd_list.asp?tid=%s&urlstr=phot&list_type=2&board_no=%s&board_nm=%s""" % (self.pimid, seq, board_nm)
            if self.debug:  print "tool.login: �� �Խ��� ���� ��������", url
            temp = self.mycook.getPage(url, cookie_select=self.mycook.cookie_photo, host="minihp.cyworld.com",
                                 language="ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4", charset="windows-949,utf-8;q=0.7,*;q=0.3",
                                 accept="application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
            
            # �Խñ� ���� ���ϱ�...
            if self.debug:
                open("after_login_���Խ��Ƿε���.html", "w").write(temp)
            count = 0
            try:
                count = re.compile("""�Դϴ�.+\((\d+)\)""").findall(temp)[0]
            except:
                pass


            folderList.append({"url":url, "name":real_nm.strip(), "count":count, "board_nm":board_nm, "seq":seq})


            # recent page no ó��, dict �ʱ�ȭ (��� Ű�� ��������)
            if not self.config.recentlyPageNo.has_key(real_nm):
                self.config.recentlyPageNo[real_nm] = -1



##            folderList.reverse()
        self.mainStatusBar.SetLabel("�α��� ����")

    except Exception, msg:
        if self.debug:
            traceback.print_exc(file=sys.stdout)
##                    print msg
##                    print param

        self.mainStatusBar.SetLabel("����ø ���� ����Ʈ�� ���������� ������ �߻��Ͽ����ϴ�. �ٽ� �õ��غ�����.")
        return False

    return folderList








def loadConfig(self, version=""):
        """ config ��ü�� ������ �о� ȭ�鿡 ��Ÿ�� """

        self.cyLoginEmailTxt.SetValue(self.config.cyLogin)

def saveConfig(self, version = ""):
    self.config.cyLogin = self.cyLoginEmailTxt.GetValue()
    self.config.version = version

    Config.saveConfig(self.config)



def setButtonState(self, state):
    """ stateNum�� ���� �� ��ư���� Ȱ��ȭ ���¸� ������ """

    if self.debug:
##        print "tools.setButtonState: menu.isEnabled()", self.subMenu.Enable(self.optionMenuID, False)
        pass


    if state == self.STATE_INIT:
        self.cyLoginBtn.Enable(True)
        self.startBtn.Enable(False)
        self.pcdownBtn.Enable(False)
        self.stopBtn.Enable(False)
        self.subMenu.Enable(self.optionMenuID, True)

    elif state == self.STATE_LOGGED:
        self.cyLoginBtn.Enable(False)
        self.startBtn.Enable(True)
        self.pcdownBtn.Enable(True)
        self.stopBtn.Enable(False)
        self.subMenu.Enable(self.optionMenuID, True)

    elif state == self.STATE_STARTED:
        self.cyLoginBtn.Enable(False)
        self.startBtn.Enable(False)
        self.pcdownBtn.Enable(False)
        self.stopBtn.Enable(True)
        self.subMenu.Enable(self.optionMenuID, False)
        
    elif state == self.STATE_NOWLOGING:
        self.cyLoginBtn.Enable(False)
        self.startBtn.Enable(False)
        self.pcdownBtn.Enable(False)
        self.stopBtn.Enable(False)
        self.subMenu.Enable(self.optionMenuID, False)


def initChkListBox(self, refresh=False):
    import math


    for idx, folder in enumerate(self.folderList):
        if refresh:
            self.folderListChkListBox.SetString(idx, "%s (%s, %d/%d)" % (folder["name"], folder["count"], self.config.recentlyPageNo.get(folder["name"], -1),int(math.ceil(int(folder["count"]) / 20.0))))
        else:
            self.folderListChkListBox.Append("%s (%s, %d/%d)" % (folder["name"], folder["count"], self.config.recentlyPageNo.get(folder["name"], -1),int(math.ceil(int(folder["count"]) / 20.0))))




    self.folderListChkListBox.Refresh()




def stoppedByUser(self, msg=""):
    self.garbageCollector()

    try:
        setButtonState(self.parent, self.parent.STATE_LOGGED)
        self.parent.mainStatusBar.SetLabel("����ڿ� ���� �۾��� ���� �Ǿ����ϴ�." if msg == "" else msg)
        self.parent.monitoringTimer.Stop()
        self.parent.downloader.isRunning = False
        self.parent.uploader.isRunning = False
        self.parent.downloader = None
        self.parent.uploader = None

        tools.saveConfig(self, version)


    except:
        pass












if __name__ == "__main__":
    # login test code....
    import os, re, httplib, time

    #import psyco
    #psyco.full()
    #psyco.profile(0.0)

    from config import Config
    from picture import Picture
    from threading import Thread
    import tools
    import time

    h = httplib.HTTP("minihp.cyworld.com")
    h.putrequest('GET', url)
    h.putheader('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    h.putheader("Accept-Language", "ko")
    h.putheader("Accept-Encoding", "gzip, deflate")
    h.putheader("Accept-Charset", "EUC-KR,utf-8;q=0.7,*;q=0.7")
    h.putheader("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)")
    h.putheader("Host", "minihp.cyworld.com")
    h.putheader("Connection", "Keep-Alive")
    h.putheader("Keep-Alive", "30")
    h.putheader("Cookie", self.cookie)
    h.endheaders()
    errorCode, errorMessage, headers = h.getreply()
##        if self.parent.debug:   print errorCode, errorMessage, headers

    result = h.file.read()

    pass


















