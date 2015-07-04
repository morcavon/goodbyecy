# -*- coding: mbcs -*-
#-----------------------------------------------------------------------------
# Name:        mainFrame.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/27
# Version:     0.3.115
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------
#Boa:Frame:Frame1

version = "0.3.115"

import wx


#import psyco
#psyco.full()
#psyco.profile(0.0)



import icon
import tools
import re, time, os
from about import About
from optionDlg import OptionDialog
from config import Config
from picture import Picture
from downloader import Downloader
from uploader import Uploader




def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BLOGPASSWORDTXT, wxID_FRAME1CYLOGINBTN, 
 wxID_FRAME1CYLOGINEMAILTXT, wxID_FRAME1CYLOGINPASSWORDTXT, 
 wxID_FRAME1FOLDERLISTCHKLISTBOX, wxID_FRAME1MAINPROGRESSBAR, 
 wxID_FRAME1MAINSTATUSBAR, wxID_FRAME1PCDOWNBTN, wxID_FRAME1PREVIEWBITMAP, 
 wxID_FRAME1PREVIEWCHECKBOX, wxID_FRAME1SELECTALLCHKBOX, 
 wxID_FRAME1SELECTTARGETDIRBTN, wxID_FRAME1STARTBTN, wxID_FRAME1STATICBOX1, 
 wxID_FRAME1STATICTEXT1, wxID_FRAME1STATICTEXT2, wxID_FRAME1STATICTEXT3, 
 wxID_FRAME1STOPBTN, wxID_FRAME1TARGETDIRTEXT, 
] = [wx.NewId() for _init_ctrls in range(20)]

[wxID_FRAME1SUBMENUSUB_ABOUT_MENU, wxID_FRAME1SUBMENUSUB_OPTION_MENU, 
] = [wx.NewId() for _init_coll_subMenu_Items in range(2)]

[wxID_FRAME1MONITORINGTIMER] = [wx.NewId() for _init_utils in range(1)]

class Frame1(wx.Frame):
    ##################################################################
    ################## Constants ####################################
    STATE_INIT = 1
    STATE_LOGGED = 2
    STATE_STARTED = 3
    STATE_NOWLOGING = 4

    def _init_coll_mainMenubar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.subMenu, title='\xb8\xde\xb4\xba')

    def _init_coll_subMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1SUBMENUSUB_OPTION_MENU,
              kind=wx.ITEM_NORMAL, text='\xbf\xc9\xbc\xc7')
        parent.Append(help='', id=wxID_FRAME1SUBMENUSUB_ABOUT_MENU,
              kind=wx.ITEM_NORMAL, text='\xb8\xb8\xb5\xe7\xc0\xcc')
        self.Bind(wx.EVT_MENU, self.OnSubMenuSub_option_menuMenu,
              id=wxID_FRAME1SUBMENUSUB_OPTION_MENU)
        self.Bind(wx.EVT_MENU, self.OnSubMenuSub_about_menuMenu,
              id=wxID_FRAME1SUBMENUSUB_ABOUT_MENU)

    def _init_utils(self):
        # generated method, don't edit
        self.mainMenubar = wx.MenuBar()

        self.subMenu = wx.Menu(title='')

        self.monitoringTimer = wx.Timer(id=wxID_FRAME1MONITORINGTIMER,
              owner=self)
        self.Bind(wx.EVT_TIMER, self.OnMonitoringTimerTimer,
              id=wxID_FRAME1MONITORINGTIMER)

        self._init_coll_mainMenubar_Menus(self.mainMenubar)
        self._init_coll_subMenu_Items(self.subMenu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(766, 379), size=wx.Size(488, 510),
              style=~wx.MAXIMIZE_BOX & ~wx.MAXIMIZE & ~wx.RESIZE_BORDER & wx.DEFAULT_FRAME_STYLE,
              title="GoodbyeCy")
        self._init_utils()
        self.SetClientSize(wx.Size(480, 483))
        self.SetBackgroundColour(wx.Colour(236, 252, 255))
        self.SetMenuBar(self.mainMenubar)
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.OnFrame1Close)

        self.cyLoginEmailTxt = wx.TextCtrl(id=wxID_FRAME1CYLOGINEMAILTXT,
              name='cyLoginEmailTxt', parent=self, pos=wx.Point(96, 16),
              size=wx.Size(160, 22), style=0, value='your@email.com')
        self.cyLoginEmailTxt.SetInsertionPoint(0)
        self.cyLoginEmailTxt.Bind(wx.EVT_CHAR, self.OnCyLoginEmailTxtChar)

        self.cyLoginPasswordTxt = wx.TextCtrl(id=wxID_FRAME1CYLOGINPASSWORDTXT,
              name='cyLoginPasswordTxt', parent=self, pos=wx.Point(96, 48),
              size=wx.Size(100, 22), style=wx.TE_PASSWORD, value='')
        self.cyLoginPasswordTxt.SetToolTipString('\xbd\xce\xc0\xcc \xb7\xce\xb1\xd7\xc0\xce \xbe\xcf\xc8\xa3. \xc0\xd3\xbd\xc3\xb7\xce \xba\xf1\xb9\xd0\xb9\xf8\xc8\xa3\xb8\xa6 \xba\xaf\xb0\xe6\xc7\xcf\xbd\xc3\xb1\xe2\xb8\xa6 \xc3\xdf\xc3\xb5\xc7\xd5\xb4\xcf\xb4\xd9.')
        self.cyLoginPasswordTxt.Bind(wx.EVT_CHAR, self.OnCyLoginPasswordTxtChar)

        self.blogPasswordTxt = wx.TextCtrl(id=wxID_FRAME1BLOGPASSWORDTXT,
              name='blogPasswordTxt', parent=self, pos=wx.Point(96, 80),
              size=wx.Size(100, 22), style=wx.TE_PASSWORD, value='')
        self.blogPasswordTxt.SetToolTipString('블로그 비밀번호(이글루스/싸이월드 블로그는 API key를 입력하세요.)')
        self.blogPasswordTxt.Bind(wx.EVT_CHAR, self.OnBlogPasswordTxtChar)

        self.cyLoginBtn = wx.Button(id=wxID_FRAME1CYLOGINBTN,
              label='\xb7\xce\xb1\xd7\xc0\xce \xb9\xd7 \xbb\xe7\xc1\xf8\xc3\xb8 \xc1\xa4\xba\xb8 \xb0\xa1\xc1\xae\xbf\xc0\xb1\xe2',
              name='cyLoginBtn', parent=self, pos=wx.Point(264, 16),
              size=wx.Size(208, 32), style=0)
        self.cyLoginBtn.Bind(wx.EVT_BUTTON, self.OnCyLoginBtnButton,
              id=wxID_FRAME1CYLOGINBTN)
        self.cyLoginBtn.Bind(wx.EVT_CHAR, self.OnCyLoginBtnChar)

        self.startBtn = wx.Button(id=wxID_FRAME1STARTBTN,
              label='\xba\xed\xb7\xce\xb1\xd7\xb7\xce \xbf\xc3\xb8\xae\xb1\xe2',
              name='startBtn', parent=self, pos=wx.Point(304, 224),
              size=wx.Size(128, 32), style=0)
        self.startBtn.Bind(wx.EVT_BUTTON, self.OnStartBtnButton,
              id=wxID_FRAME1STARTBTN)
        self.startBtn.Bind(wx.EVT_CHAR, self.OnStartBtnChar)

        self.stopBtn = wx.Button(id=wxID_FRAME1STOPBTN,
              label='\xb8\xd8\xc3\xe3', name='stopBtn', parent=self,
              pos=wx.Point(304, 344), size=wx.Size(80, 32), style=0)
        self.stopBtn.Bind(wx.EVT_BUTTON, self.OnStopBtnButton,
              id=wxID_FRAME1STOPBTN)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=' Blog \xba\xf1\xb9\xd0\xb9\xf8\xc8\xa3',
              name='staticText1', parent=self, pos=wx.Point(8, 80),
              size=wx.Size(79, 14), style=0)

        self.staticText2 = wx.StaticText(id=wxID_FRAME1STATICTEXT2,
              label='       \xba\xf1\xb9\xd0\xb9\xf8\xc8\xa3',
              name='staticText2', parent=self, pos=wx.Point(8, 48),
              size=wx.Size(76, 14), style=0)

        self.staticText3 = wx.StaticText(id=wxID_FRAME1STATICTEXT3,
              label='Cy e-mail ID', name='staticText3', parent=self,
              pos=wx.Point(8, 16), size=wx.Size(64, 14), style=0)

        self.mainStatusBar = wx.StatusBar(id=wxID_FRAME1MAINSTATUSBAR,
              name='mainStatusBar', parent=self, style=0)
        self.mainStatusBar.SetMinSize(wx.Size(420, 20))
        self.SetStatusBar(self.mainStatusBar)

        self.mainProgressbar = wx.Gauge(id=wxID_FRAME1MAINPROGRESSBAR,
              name='mainProgressbar', parent=self, pos=wx.Point(278, 128),
              range=100, size=wx.Size(18, 288),
              style=wx.GA_VERTICAL | wx.GA_PROGRESSBAR | wx.GA_SMOOTH | wx.GA_HORIZONTAL)
        self.mainProgressbar.SetMinSize(wx.Size(300, 20))
        self.mainProgressbar.SetAutoLayout(False)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME1STATICBOX1,
              label='\xbb\xe7\xc1\xf8\xc3\xb8 \xc6\xfa\xb4\xf5',
              name='staticBox1', parent=self, pos=wx.Point(8, 120),
              size=wx.Size(256, 320), style=0)

        self.folderListChkListBox = wx.CheckListBox(choices=[],
              id=wxID_FRAME1FOLDERLISTCHKLISTBOX, name='folderListChkListBox',
              parent=self, pos=wx.Point(16, 144), size=wx.Size(240, 288),
              style=wx.LB_SINGLE | wx.LB_HSCROLL | wx.VSCROLL | wx.HSCROLL)
        self.folderListChkListBox.SetToolTipString('\xb0\xfd\xc8\xa3\xbe\xc8\xc0\xc7 \xbc\xfd\xc0\xda\xb4\xc2 (\xc3\xd1 \xb0\xd4\xbd\xc3\xb9\xb0 \xbc\xf6, \xc3\xd6\xb1\xd9\xbf\xa1 \xc6\xf7\xbd\xba\xc6\xc3\xb5\xc8 \xc6\xe4\xc0\xcc\xc1\xf6 \xb9\xf8\xc8\xa3/\xc0\xfc\xc3\xbc \xc6\xe4\xc0\xcc\xc1\xf6\xbc\xf6)\xc0\xd4\xb4\xcf\xb4\xd9.\n\n\xc3\xd6\xb1\xd9\xbf\xa1 \xc6\xf7\xbd\xba\xc6\xc3\xb5\xc8 \xc6\xe4\xc0\xcc\xc1\xf6 \xb9\xf8\xc8\xa3\xb0\xa1 "0"\xc0\xcc\xb8\xe9 \xc7\xd8\xb4\xe7 \xc6\xfa\xb4\xf5 \xbe\xf7\xb7\xce\xb5\xe5 \xbf\xcf\xb7\xe1\xb8\xa6 \xb6\xe6\xc7\xcf\xb8\xe7, "-1"\xc0\xcc\xb8\xe9 \xbe\xc6\xc1\xf7 \xc0\xdb\xbe\xf7\xc0\xbb \xbd\xc3\xc0\xdb\xc7\xcf\xc1\xf6 \xbe\xca\xbe\xd2\xb4\xd9\xb4\xc2 \xc0\xc7\xb9\xcc\xc0\xd4\xb4\xcf\xb4\xd9.\n(\xb8\xb6\xc1\xf6\xb8\xb7 \xc6\xe4\xc0\xcc\xc1\xf6\xba\xce\xc5\xcd \xc0\xdb\xbe\xf7 \xc7\xd1\xb4\xd9\xb4\xc2\xb0\xcd\xbf\xa1 \xc0\xaf\xc0\xc7\xc7\xcf\xbc\xbc\xbf\xe4)')
        self.folderListChkListBox.SetStringSelection('')
        self.folderListChkListBox.SetHelpText('')

        self.selectAllChkbox = wx.CheckBox(id=wxID_FRAME1SELECTALLCHKBOX,
              label='\xc0\xfc\xc3\xbc\xbc\xb1\xc5\xc3/\xc7\xd8\xc1\xa6',
              name='selectAllChkbox', parent=self, pos=wx.Point(272, 424),
              size=wx.Size(120, 14), style=0)
        self.selectAllChkbox.SetValue(False)
        self.selectAllChkbox.Bind(wx.EVT_CHECKBOX,
              self.OnSelectAllChkboxCheckbox, id=wxID_FRAME1SELECTALLCHKBOX)

        self.previewCheckBox = wx.CheckBox(id=wxID_FRAME1PREVIEWCHECKBOX,
              label='\xb9\xcc\xb8\xae\xba\xb8\xb1\xe2', name='previewCheckBox',
              parent=self, pos=wx.Point(304, 136), size=wx.Size(79, 14),
              style=0)
        self.previewCheckBox.SetValue(False)
        self.previewCheckBox.SetToolTipString('\xc7\xf6\xc0\xe7 \xb4\xd9\xbf\xee\xb9\xde\xb0\xed \xc0\xd6\xb4\xc2 \xbb\xe7\xc1\xf8\xc0\xbb \xba\xb8\xbf\xa9\xc1\xdd\xb4\xcf\xb4\xd9...')
        self.previewCheckBox.Bind(wx.EVT_CHECKBOX,
              self.OnPreviewCheckBoxCheckbox, id=wxID_FRAME1PREVIEWCHECKBOX)

        self.pcdownBtn = wx.Button(id=wxID_FRAME1PCDOWNBTN,
              label='PC\xb7\xce \xb4\xd9\xbf\xee\xb7\xce\xb5\xe5',
              name='pcdownBtn', parent=self, pos=wx.Point(304, 272),
              size=wx.Size(128, 32), style=0)
        self.pcdownBtn.Bind(wx.EVT_BUTTON, self.OnPcdownBtnButton,
              id=wxID_FRAME1PCDOWNBTN)

        self.previewBitmap = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_FRAME1PREVIEWBITMAP, name='previewBitmap', parent=self,
              pos=wx.Point(496, 24), size=wx.Size(392, 408), style=0)
        self.previewBitmap.SetToolTipString('\xc7\xf6\xc0\xe7 \xb4\xd9\xbf\xee\xb7\xce\xb5\xe5\xc1\xdf\xc0\xce \xbb\xe7\xc1\xf8...')

        self.targetDirText = wx.TextCtrl(id=wxID_FRAME1TARGETDIRTEXT,
              name='targetDirText', parent=self, pos=wx.Point(264, 64),
              size=wx.Size(208, 22), style=wx.TE_READONLY, value='')

        self.selectTargetDirBtn = wx.Button(id=wxID_FRAME1SELECTTARGETDIRBTN,
              label='\xb4\xd9\xbf\xee\xb9\xde\xc0\xbb \xc6\xfa\xb4\xf5 \xbc\xb1\xc5\xc3',
              name='selectTargetDirBtn', parent=self, pos=wx.Point(264, 88),
              size=wx.Size(128, 24), style=0)
        self.selectTargetDirBtn.SetToolTipString('PC\xb7\xce \xb4\xd9\xbf\xee\xb9\xde\xc0\xbb \xb0\xe6\xbf\xec\xbf\xa1 \xc6\xfa\xb4\xf5\xb8\xa6 \xbc\xb1\xc5\xc3\xc7\xcf\xbc\xbc\xbf\xe4.')
        self.selectTargetDirBtn.Bind(wx.EVT_BUTTON,
              self.OnSelectTargetDirBtnButton,
              id=wxID_FRAME1SELECTTARGETDIRBTN)

    def __init__(self, parent):
        self._init_ctrls(parent)

        ##################################################################
        ################## Debug mode ####################################
        self.debug = True if os.environ.has_key("CYDEBUG") else False


        ##################################################################
        ################## global variables ##############################
        self.config = Config.getConfig(version)

        self.isRunning = False
        self.folderList = []
        self.pictureList = []
        self.downloader = None          # cy -> pc
        self.uploader = None            # pc -> blog
        self.pimid = ""
        self.optionMenuID = wxID_FRAME1SUBMENUSUB_OPTION_MENU
        self.mycook = None              # my cook instance...
        self.targetDir = ""




        ##################################################################
        ################## Update check ##################################
        if Config.checkNewVersion(version, self.debug):
            dlg = wx.SingleChoiceDialog(self, '새 버전이 올라왔습니다. 블로그로 이동하시겠습니까?', '새 버전 확인', ["예", "아니오"])
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    selected = dlg.GetStringSelection()
                    if selected == "예":
                        try:
                            import webbrowser
                            webbrowser.open("""http://www.morcavon.com/1178440402""")
                            self.Close()
                            return
                        except:
                            pass

            finally:
                dlg.Destroy()



        ##################################################################
        ################## 메인 창 스타일 ################################
        self.SetIcon(wx.IconFromBitmap(icon.getBitmap()))
        self.mainTitle = "GoodbyeCy Ver.%s" % version
        self.SetLabel(self.mainTitle)
        self.mainStatusBar.SetLabel(self.mainTitle)






        ##################################################################
        ################## initializing ##################################
        tools.loadConfig(self)


        # 디버깅 정보
        if self.debug:
            self.cyLoginEmailTxt.SetValue(os.environ["CYID"])
            self.cyLoginPasswordTxt.SetValue(os.environ["CYPASSWORD"])
            #self.blogPasswordTxt.SetValue(os.environ["BLOG_API_PASSWORD"])
            #self.targetDir = os.environ["PCDOWN_DIR"]
            


        tools.setButtonState(self, self.STATE_INIT)
        self.monitoringTimer.Stop()




        ##################################################################
        ################## 사용자 동의 확인 ##################################
        if not self.debug:
            dlg = wx.MessageDialog(self, '안전한 사용을 위해 비밀번호를 임시로 변경한뒤 사용하세요.', '알림', wx.OK | wx.ICON_INFORMATION)
            try:
                result = dlg.ShowModal()
            finally:
                dlg.Destroy()


        ##################################################################
        ################## JQuery file checking ##########################
        self.check_jquery()
        




    ##################################################################
    ################## 컨트롤 이벤트 처리 함수 #######################

    def OnCyLoginBtnButton(self, event):
        if self.cyLoginEmailTxt.GetValue() == "" or self.cyLoginPasswordTxt.GetValue() == "":
            dlg = wx.MessageDialog(self, 'Cy 로그인 정보를 입력하세요.', '알림', wx.OK | wx.ICON_ERROR)
            try:
                result = dlg.ShowModal()
            finally:
                dlg.Destroy()
                return


        # 로그인 프로세스
        tools.setButtonState(self, self.STATE_NOWLOGING)
        self.folderList = tools.login(self)

        if self.folderList == False:
            dlg = wx.MessageDialog(self, self.mainStatusBar.GetLabel(), '로그인 중 오류가 발생하였습니다.', wx.OK | wx.ICON_ERROR)
            try:
                result = dlg.ShowModal()
            finally:
                dlg.Destroy()
                tools.setButtonState(self, self.STATE_INIT)
                return
        elif self.folderList == []:
            return



        tools.initChkListBox(self)

        tools.setButtonState(self, self.STATE_LOGGED)
        self.isRunning = False

        #----------------- 로그인 성공------------------
        self.mainStatusBar.SetLabel("싸이 로그인 성공")



        event.Skip()






    def OnPcdownBtnButton(self, event):
        """ 다운받은 이미지를 로컬 PC에 저장 (cyro) """
        
        # 폴더 선택 여부 체크
        if self.targetDir == "":
            dlg = wx.MessageDialog(self, '사진을 저장할 폴더를 먼저 선택하세요.', '알림', wx.OK | wx.ICON_INFORMATION)
            try:
                result = dlg.ShowModal()
                self.selectTargetDirBtn.SetFocus()
                return
            finally:
                dlg.Destroy()
        
        
        temp = open("goodbyeCy.log", "w")
        temp.close()
        tools.setButtonState(self, self.STATE_STARTED)
        self.isRunning = True

        self.downloader = Downloader(self, True)

        # down/up loader 동시에 실행....producer/consumer 모델 참조....
        self.downloader.start()

        self.monitoringTimer.Start(1000)
        event.Skip()






    def OnStartBtnButton(self, event):
        import xmlrpclib

        # 블로그 암호 입력 여부 체크
        if self.blogPasswordTxt.GetValue() == "":
            dlg = wx.MessageDialog(self, '블로그 비밀번호를 입력하세요.', '오류', wx.OK | wx.ICON_ERROR)
            try:
                result = dlg.ShowModal()
            finally:
                dlg.Destroy()
                return


        # blog API 접속 검증
        try:
            self.server =  xmlrpclib.Server(self.config.blogAPI["address"])
        except Exception, msg:
            if self.debug:  print "mainFrame:onStart", msg, self.config.blogAPI

            dlg = wx.MessageDialog(self, '블로그 API 서버 접속에 문제가 있습니다. API 주소와 ID, 비밀번호등을 다시 확인해주세요.', '오류', wx.OK | wx.ICON_ERROR)
            try:
                result = dlg.ShowModal()
            finally:
                dlg.Destroy()
                return


        # 이어하기 할지 여부 선택
        for el in self.config.recentlyPageNo.values():
            # 하나라도 로깅된게 있으면 이어하기
            if el >= 0:
                dlg = wx.MessageDialog(self, '기존에 포스팅을 했던 폴더가 있습니다. 이어서 하시겠습니까?\r\n (예를 선택하면 포스팅이 모두 완료되었던 폴더는 건너뜁니다. 아니오를 선택하면 처음부터 다시 시작합니다)', '알림', wx.YES_NO | wx.ICON_INFORMATION)
                try:
                    result = dlg.ShowModal()


                    if result == wx.ID_YES:
                        if self.debug:  print "do continue"
                        pass
                    else:

                        # dict 초기화
                        for k in self.config.recentlyPageNo.keys():
                            self.config.recentlyPageNo[k] = -1

                        if self.debug:  print "do not continue"

                    tools.initChkListBox(self, True)
                finally:
                    dlg.Destroy()

                break


        temp = open("goodbyeCy.log", "w")
        temp.close()
        tools.setButtonState(self, self.STATE_STARTED)
        self.isRunning = True

        self.downloader = Downloader(self)
        self.uploader = Uploader(self)

        # down/up loader 동시에 실행....producer/consumer 모델 참조....
        self.downloader.start()
        self.uploader.start()

        self.monitoringTimer.Start(1000)



    def OnSelectTargetDirBtnButton(self, event):
        dlg = wx.DirDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.targetDir = dlg.GetPath()
                self.targetDirText.SetValue(self.targetDir)
        finally:
            dlg.Destroy()
        event.Skip()





    def OnStopBtnButton(self, event):
        tools.setButtonState(self, self.STATE_LOGGED)
        self.isRunning = False
        self.downloader.isRunning = False
        if self.uploader!= None: self.uploader.isRunning = False
        self.mainStatusBar.SetLabel("사용자에 의해 작업이 중지 되었습니다.")
        self.monitoringTimer.Stop()
        self.downloader = None
        self.uploader = None



    def OnSubMenuSub_option_menuMenu(self, event):
        dlg = OptionDialog(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                """ 새로 설정된 옵션을 파일에 저장 """
                Config.saveConfig(self.config)

        finally:
            dlg.Destroy()


    def OnSubMenuSub_about_menuMenu(self, event):
        dlg = About(self)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                pass
        finally:
            dlg.Destroy()



    def OnFrame1Close(self, event):
        """ 프로그램 종료시 처리해야 할것들... """

        if self.debug:
            print "closing....begin"

        tools.saveConfig(self, version)
        self.monitoringTimer.Stop()

        self.isRunning = False
        if self.downloader != None: self.downloader.isRunning = False
        if self.uploader != None: self.uploader.isRunning = False


        if self.debug:
            print "closed...end"

        time.sleep(0.5)


        event.Skip()



    def OnSelectAllChkboxCheckbox(self, event):
        """ 전체 선택/해체 """
        for id in range(len(self.folderListChkListBox.GetItems())):
            self.folderListChkListBox.Check(id, event.Checked())

        event.Skip()
        
        
        
        
    def OnPreviewCheckBoxCheckbox(self, event):
        """ 다운중인 이미지 미리보기 처리 """
        if self.previewCheckBox.GetValue():
            self.SetClientSize(wx.Size(900, self.GetClientSize().y))
        else:
            self.SetClientSize(wx.Size(480, self.GetClientSize().y))
        event.Skip()





    def OnMonitoringTimerTimer(self, event):
        """ 주기적으로 작업 상태를 모니터링하여 상태바/프로그레스바에 나타냄"""
        if self.downloader != None or self.uploader != None:
            downloadedCount = self.downloader.downloadedCount if self.downloader != None else 0
            uploadedCount = self.uploader.postedCount if self.uploader != None else 0
            totalCount = self.downloader.totalPictureCount*2 if self.uploader != None else self.downloader.totalPictureCount

            progressPercentage = float(downloadedCount + uploadedCount) / float(totalCount) * 100.0 if totalCount > 0 else 0.0
            currentFolderName = self.downloader.currentFolder
            currentUploadingFolderName = self.uploader.currentUploadingFolder if self.uploader != None else ""

            self.mainProgressbar.SetValue(int(progressPercentage))
            self.mainStatusBar.SetLabel("[%s] 다운로드 / [%s] 포스팅 중..." % (currentFolderName, currentUploadingFolderName))

            if self.debug:
                print "Current %d / %d, %d%% (%s)" % (downloadedCount  + uploadedCount, totalCount, progressPercentage, currentFolderName)

        
        ############ 작업 정상 종료 체크 ############
        if (self.uploader == None and self.downloader.isRunning == False) or (self.uploader != None and self.uploader.isRunning == False):
            tools.setButtonState(self, self.STATE_LOGGED)
            self.isRunning = False
            self.downloader.isRunning = False
            if self.uploader != None: self.uploader.isRunning = False
            self.mainStatusBar.SetLabel("모든 작업이 종료되었습니다.")
            self.monitoringTimer.Stop()
            self.downloader = None
            self.uploader = None
            tools.saveConfig(self, version)



        event.Skip()




    ############################## TAB TRAVERSAL 용 ########################
    ########################################################################
    def OnCyLoginEmailTxtChar(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            self.cyLoginPasswordTxt.SetFocus()
        event.Skip()

    def OnCyLoginPasswordTxtChar(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            self.blogPasswordTxt.SetFocus()
        event.Skip()

    def OnBlogPasswordTxtChar(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            self.cyLoginBtn.SetFocus()
        event.Skip()

    def OnCyLoginBtnChar(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            self.startBtn.SetFocus()
        event.Skip()

    def OnStartBtnChar(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            self.cyLoginEmailTxt.SetFocus()
        event.Skip()


    ########################################################################
    ########################################################################

    def check_jquery(self):
        import urllib
        jq_list = {"jquery-1.5.2.js":"http://code.jquery.com/jquery-1.5.2.js", 
                   "jquery.simulate.js":"http://jqueryjs.googlecode.com/svn-history/r6063/trunk/plugins/simulate/jquery.simulate.js", 
                   "jquery.min.js":"http://code.jquery.com/jquery-1.5.2.min.js"}
        
        if not os.path.exists("javascript"):
            os.mkdir("javascript")
        
        for f, u in jq_list.items():
            try:
                fullpath = os.path.join("javascript", f)
                if not os.path.exists(fullpath):
                    urllib.urlretrieve(u, fullpath)
                    
            except Exception, msg:
                if self.debug:
                    print "Exception: ", msg
                    traceback.print_exc(file=sys.stdout)
                self.errmsg = "jquery 파일 다운에 실패하였습니다. 인터넷 연결을 확인하세요..."
                return
                 













if __name__ == "__main__":
    import os
    if os.path.exists("GoodbyeCy.py"):
        os.system("GoodbyeCy.py")
    else:
        os.system("GoodbyeCy.pyw")
