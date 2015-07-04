# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        optionDlg.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/28
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------
#Boa:Frame:OptionDialog

import wx
from config import Config

def create(parent):
    return OptionDialog(parent)

[wxID_OPTIONDIALOG, wxID_OPTIONDIALOGBLOGAPIADDRESSTXT, 
 wxID_OPTIONDIALOGBLOGAPIIDTXT, wxID_OPTIONDIALOGBLOGAPIUSERIDTXT, 
 wxID_OPTIONDIALOGCANCELBTN, wxID_OPTIONDIALOGCATEGORYNAMETXT, 
 wxID_OPTIONDIALOGDOSYNCDATECHKBOX, wxID_OPTIONDIALOGGETCOMMENTSCHKBOX, 
 wxID_OPTIONDIALOGMAXITEMCNTSPIN, wxID_OPTIONDIALOGNONPUBLICPOLICYCMBBOX, 
 wxID_OPTIONDIALOGOKBTN, wxID_OPTIONDIALOGPUBLICPOLICYCMBBOX, 
 wxID_OPTIONDIALOGRESTRICTEDPUBLICPOLICYCMBBOX, wxID_OPTIONDIALOGSTATICBOX1, 
 wxID_OPTIONDIALOGSTATICBOX2, wxID_OPTIONDIALOGSTATICBOX3, 
 wxID_OPTIONDIALOGSTATICLINE1, wxID_OPTIONDIALOGSTATICTEXT1, 
 wxID_OPTIONDIALOGSTATICTEXT10, wxID_OPTIONDIALOGSTATICTEXT11, 
 wxID_OPTIONDIALOGSTATICTEXT12, wxID_OPTIONDIALOGSTATICTEXT13, 
 wxID_OPTIONDIALOGSTATICTEXT2, wxID_OPTIONDIALOGSTATICTEXT3, 
 wxID_OPTIONDIALOGSTATICTEXT4, wxID_OPTIONDIALOGSTATICTEXT5, 
 wxID_OPTIONDIALOGSTATICTEXT6, wxID_OPTIONDIALOGSTATICTEXT7, 
 wxID_OPTIONDIALOGSTATICTEXT8, wxID_OPTIONDIALOGSTATICTEXT9, 
] = [wx.NewId() for _init_ctrls in range(30)]

class OptionDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_OPTIONDIALOG, name='Option',
              parent=prnt, pos=wx.Point(686, 383), size=wx.Size(418, 572),
              style=wx.SYSTEM_MENU | wx.DEFAULT_DIALOG_STYLE,
              title='\xbf\xc9\xbc\xc7')
        self.SetClientSize(wx.Size(400, 525))
        self.SetBackgroundColour(wx.Colour(254, 249, 226))
        self.Bind(wx.EVT_INIT_DIALOG, self.OnOptionDialogInitDialog)
        self.Bind(wx.EVT_CLOSE, self.OnOptionDialogClose)

        self.blogAPIAddressTxt = wx.TextCtrl(id=wxID_OPTIONDIALOGBLOGAPIADDRESSTXT,
              name='blogAPIAddressTxt', parent=self, pos=wx.Point(56, 32),
              size=wx.Size(240, 22), style=0, value='')
        self.blogAPIAddressTxt.SetToolTipString('\xba\xed\xb7\xce\xb1\xd7 API\xc0\xc7 \xc1\xd6\xbc\xd2\xb8\xa6 \xc0\xd4\xb7\xc2\xc7\xcf\xbc\xbc\xbf\xe4.')

        self.blogAPIIdTxt = wx.TextCtrl(id=wxID_OPTIONDIALOGBLOGAPIIDTXT,
              name='blogAPIIdTxt', parent=self, pos=wx.Point(66, 64),
              size=wx.Size(100, 22), style=0, value='')
        self.blogAPIIdTxt.SetToolTipString('\xba\xed\xb7\xce\xb1\xd7 API\xc0\xc7 ID\xb8\xa6 \xc0\xd4\xb7\xc2\xc7\xcf\xbc\xbc\xbf\xe4.\n(\xc0\xcc\xb1\xdb\xb7\xe7\xbd\xba\xbf\xa1\xbc\xad\xb4\xc2 \xc7\xca\xbf\xe4\xc7\xcf\xc1\xf6 \xbe\xca\xbd\xc0\xb4\xcf\xb4\xd9)')

        self.blogAPIUserIDtxt = wx.TextCtrl(id=wxID_OPTIONDIALOGBLOGAPIUSERIDTXT,
              name='blogAPIUserIDtxt', parent=self, pos=wx.Point(272, 64),
              size=wx.Size(100, 22), style=0, value='')
        self.blogAPIUserIDtxt.SetToolTipString('블로그 로그인 ID (싸이월드블로그는 Blog ID와 동일함)')

        self.nonpublicPolicyCmbbox = wx.ComboBox(choices=["공개", "비공개"],
              id=wxID_OPTIONDIALOGNONPUBLICPOLICYCMBBOX,
              name='nonpublicPolicyCmbbox', parent=self, pos=wx.Point(256, 160),
              size=wx.Size(130, 22), style=wx.CB_READONLY,
              value='\xba\xf1\xb0\xf8\xb0\xb3')
        self.nonpublicPolicyCmbbox.SetLabel('\xba\xf1\xb0\xf8\xb0\xb3')

        self.restrictedpublicPolicyCmbbox = wx.ComboBox(choices=["공개",
              "비공개"], id=wxID_OPTIONDIALOGRESTRICTEDPUBLICPOLICYCMBBOX,
              name='restrictedpublicPolicyCmbbox', parent=self,
              pos=wx.Point(256, 184), size=wx.Size(130, 22),
              style=wx.CB_READONLY, value='\xba\xf1\xb0\xf8\xb0\xb3')
        self.restrictedpublicPolicyCmbbox.SetLabel('\xba\xf1\xb0\xf8\xb0\xb3')

        self.publicPolicyCmbbox = wx.ComboBox(choices=["공개", "비공개"],
              id=wxID_OPTIONDIALOGPUBLICPOLICYCMBBOX, name='publicPolicyCmbbox',
              parent=self, pos=wx.Point(256, 208), size=wx.Size(130, 22),
              style=wx.CB_READONLY, value='\xb0\xf8\xb0\xb3')
        self.publicPolicyCmbbox.SetLabel('\xb0\xf8\xb0\xb3')

        self.getCommentsChkbox = wx.CheckBox(id=wxID_OPTIONDIALOGGETCOMMENTSCHKBOX,
              label='\xb4\xf1\xb1\xdb \xc6\xf7\xc7\xd4\xc7\xd8\xbc\xad \xc0\xcc\xc0\xfc\xc7\xcf\xb1\xe2',
              name='getCommentsChkbox', parent=self, pos=wx.Point(16, 280),
              size=wx.Size(208, 14), style=0)
        self.getCommentsChkbox.SetValue(False)

        self.doSyncDateChkbox = wx.CheckBox(id=wxID_OPTIONDIALOGDOSYNCDATECHKBOX,
              label='\xbf\xf8\xba\xbb \xb0\xd4\xbd\xc3\xb9\xb0\xc0\xc7 \xc0\xdb\xbc\xba \xbd\xc3\xb0\xa3 \xc0\xaf\xc1\xf6',
              name='doSyncDateChkbox', parent=self, pos=wx.Point(16, 304),
              size=wx.Size(192, 14), style=0)
        self.doSyncDateChkbox.SetValue(False)
        self.doSyncDateChkbox.SetToolTipString('\xbe\xf7\xb7\xce\xb5\xe5 \xc7\xd2 \xc6\xf7\xbd\xba\xc6\xae\xc0\xc7 \xc0\xdb\xbc\xba \xbd\xc3\xb0\xa3\xc0\xbb \xbf\xf8\xba\xbb \xb0\xd4\xbd\xc3\xb9\xb0\xc0\xc7 \xc0\xdb\xbc\xba \xbd\xc3\xb0\xa3\xc0\xb8\xb7\xce \xc7\xd5\xb4\xcf\xb4\xd9.')

        self.categoryNameTxt = wx.TextCtrl(id=wxID_OPTIONDIALOGCATEGORYNAMETXT,
              name='categoryNameTxt', parent=self, pos=wx.Point(104, 344),
              size=wx.Size(100, 22), style=0, value='\xbb\xe7\xc1\xf8\xc3\xb8')
        self.categoryNameTxt.SetToolTipString('\xba\xed\xb7\xce\xb1\xd7\xbf\xa1\xbc\xad \xbb\xe7\xbf\xeb\xc7\xd2 \xb4\xeb\xba\xd0\xb7\xf9 \xc0\xcc\xb8\xa7\xc0\xbb \xc0\xd4\xb7\xc2\xc7\xcf\xbd\xc3\xb0\xed,\n\xba\xed\xb7\xce\xb1\xd7\xbf\xa1 \xc1\xf7\xc1\xa2 \xc4\xab\xc5\xd7\xb0\xed\xb8\xae\xb8\xa6 \xbb\xfd\xbc\xba\xc7\xcf\xbc\xbc\xbf\xe4 (\xbc\xd2\xba\xd0\xb7\xf9\xb4\xc2 \xbb\xe7\xc1\xf8\xc3\xb8 \xc6\xfa\xb4\xf5 \xc0\xcc\xb8\xa7\xc0\xb8\xb7\xce...)')

        self.staticText11 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT11,
              label='\xc4\xab\xc5\xd7\xb0\xed\xb8\xae \xc0\xcc\xb8\xa7',
              name='staticText11', parent=self, pos=wx.Point(16, 344),
              size=wx.Size(76, 40), style=0)

        self.maxItemCntSpin = wx.SpinCtrl(id=wxID_OPTIONDIALOGMAXITEMCNTSPIN,
              initial=1, max=100, min=1, name='maxItemCntSpin', parent=self,
              pos=wx.Point(248, 392), size=wx.Size(50, 22),
              style=wx.SP_ARROW_KEYS)
        self.maxItemCntSpin.SetToolTipString('2\xb0\xb3 \xc0\xcc\xbb\xf3\xc0\xc7 \xb0\xd4\xbd\xc3\xb9\xb0\xc0\xbb \xc6\xf7\xbd\xba\xc6\xae \xc7\xcf\xb3\xaa\xbf\xa1 \xc6\xf7\xc7\xd4 \xbd\xc3\xc5\xb3 \xb0\xe6\xbf\xec,\n\xc6\xf7\xbd\xba\xc6\xae\xc0\xc7 \xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4 \xb9\xd7 \xc0\xdb\xbc\xba \xbd\xc3\xb0\xa3\xc0\xba \xc3\xb9\xb9\xf8\xc2\xb0 \xb0\xd4\xbd\xc3\xb9\xb0\xc0\xc7 \xb3\xbb\xbf\xeb\xc0\xbb \xb5\xfb\xb8\xa8\xb4\xcf\xb4\xd9.')

        self.okBtn = wx.Button(id=wx.ID_OK, label='\xc8\xae\xc0\xce',
              name='okBtn', parent=self, pos=wx.Point(104, 488),
              size=wx.Size(75, 24), style=0)
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkBtnButton, id=wx.ID_OK)

        self.cancelBtn = wx.Button(id=wx.ID_CANCEL, label='\xc3\xeb\xbc\xd2',
              name='cancelBtn', parent=self, pos=wx.Point(224, 488),
              size=wx.Size(75, 24), style=0)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancelBtnButton,
              id=wx.ID_CANCEL)

        self.staticBox2 = wx.StaticBox(id=wxID_OPTIONDIALOGSTATICBOX2,
              label='\xc6\xf7\xbd\xba\xc6\xae \xb0\xf8\xb0\xb3 \xbf\xa9\xba\xce \xbc\xb3\xc1\xa4',
              name='staticBox2', parent=self, pos=wx.Point(8, 112),
              size=wx.Size(384, 128), style=0)
        self.staticBox2.SetToolTipString('\xba\xed\xb7\xce\xb1\xd7\xb7\xce \xc0\xcc\xb5\xbf\xc7\xd1 \xb0\xd4\xbd\xc3\xb9\xb0\xc0\xc7 \xb0\xf8\xb0\xb3 \xbf\xa9\xba\xce\xb8\xa6 \xbc\xb3\xc1\xa4\xc7\xd5\xb4\xcf\xb4\xd9.')

        self.staticText3 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT3,
              label='::: \xb1\xe2\xc1\xb8 \xbb\xe7\xc1\xf8\xc3\xb8 \xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4 :::',
              name='staticText3', parent=self, pos=wx.Point(24, 136),
              size=wx.Size(152, 14), style=0)
        self.staticText3.SetToolTipString('\xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4\xc0\xba \xbb\xe7\xc1\xf8\xc3\xb8 \xc6\xfa\xb4\xf5\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xcc \xbe\xc6\xb4\xd1 \xb0\xd4\xbd\xc3\xb9\xb0 \xc0\xda\xc3\xbc\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xb8\xb7\xce \xc0\xdb\xbe\xf7\xc7\xd5\xb4\xcf\xb4\xd9.')

        self.staticText4 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT4,
              label='::: \xba\xed\xb7\xce\xb1\xd7 \xc6\xf7\xbd\xba\xc6\xae \xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4 :::',
              name='staticText4', parent=self, pos=wx.Point(216, 136),
              size=wx.Size(164, 14), style=0)

        self.staticText5 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT5,
              label='\xba\xf1\xb0\xf8\xb0\xb3', name='staticText5', parent=self,
              pos=wx.Point(72, 160), size=wx.Size(36, 14), style=0)
        self.staticText5.SetToolTipString('\xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4\xc0\xba \xbb\xe7\xc1\xf8\xc3\xb8 \xc6\xfa\xb4\xf5\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xcc \xbe\xc6\xb4\xd1 \xb0\xd4\xbd\xc3\xb9\xb0 \xc0\xda\xc3\xbc\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xb8\xb7\xce \xc0\xdb\xbe\xf7\xc7\xd5\xb4\xcf\xb4\xd9.')

        self.staticText6 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT6,
              label='1\xc3\xcc\xb0\xf8\xb0\xb3', name='staticText6',
              parent=self, pos=wx.Point(64, 184), size=wx.Size(43, 14),
              style=0)
        self.staticText6.SetToolTipString('\xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4\xc0\xba \xbb\xe7\xc1\xf8\xc3\xb8 \xc6\xfa\xb4\xf5\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xcc \xbe\xc6\xb4\xd1 \xb0\xd4\xbd\xc3\xb9\xb0 \xc0\xda\xc3\xbc\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xb8\xb7\xce \xc0\xdb\xbe\xf7\xc7\xd5\xb4\xcf\xb4\xd9.')

        self.staticText7 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT7,
              label='\xc0\xfc\xc3\xbc\xb0\xf8\xb0\xb3', name='staticText7',
              parent=self, pos=wx.Point(64, 208), size=wx.Size(48, 14),
              style=0)
        self.staticText7.SetToolTipString('\xb0\xf8\xb0\xb3 \xbc\xb3\xc1\xa4\xc0\xba \xbb\xe7\xc1\xf8\xc3\xb8 \xc6\xfa\xb4\xf5\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xcc \xbe\xc6\xb4\xd1 \xb0\xd4\xbd\xc3\xb9\xb0 \xc0\xda\xc3\xbc\xc0\xc7 \xbc\xb3\xc1\xa4\xc0\xb8\xb7\xce \xc0\xdb\xbe\xf7\xc7\xd5\xb4\xcf\xb4\xd9.')

        self.staticText8 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT8,
              label='==========>', name='staticText8', parent=self,
              pos=wx.Point(136, 208), size=wx.Size(132, 19), style=0)
        self.staticText8.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText9 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT9,
              label='==========>', name='staticText9', parent=self,
              pos=wx.Point(136, 184), size=wx.Size(132, 19), style=0)
        self.staticText9.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticText10 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT10,
              label='==========>', name='staticText10', parent=self,
              pos=wx.Point(136, 160), size=wx.Size(132, 19), style=0)
        self.staticText10.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.staticBox3 = wx.StaticBox(id=wxID_OPTIONDIALOGSTATICBOX3,
              label='\xb1\xd7 \xbf\xdc...', name='staticBox3', parent=self,
              pos=wx.Point(8, 256), size=wx.Size(336, 192), style=0)

        self.staticText12 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT12,
              label='\xc6\xf7\xbd\xba\xc6\xae \xc7\xcf\xb3\xaa\xbf\xa1 \xc6\xf7\xc7\xd4\xc7\xd2 \xbb\xe7\xc1\xf8\xc3\xb8 \xb0\xd4\xbd\xc3\xb9\xb0\xc0\xc7 \xbc\xf6',
              name='staticText12', parent=self, pos=wx.Point(16, 392),
              size=wx.Size(224, 14), style=0)
        self.staticText12.SetToolTipString('\xbc\xad\xb7\xce \xb4\xd9\xb8\xa5 \xc6\xfa\xb4\xf5\xbf\xa1 \xc0\xd6\xb4\xc2 \xbb\xe7\xc1\xf8\xb5\xe9\xc0\xcc \xc7\xcf\xb3\xaa\xc0\xc7 \xc6\xf7\xbd\xba\xc6\xae\xbf\xa1 \xc6\xf7\xc7\xd4\xb5\xc9 \xb0\xe6\xbf\xec,\n\xbf\xa9\xb1\xe2\xbf\xa1 \xbc\xb3\xc1\xa4\xb5\xc8 \xb0\xaa\xb0\xfa \xbb\xf3\xb0\xfc\xbe\xf8\xc0\xcc \xba\xb0\xb0\xb3\xc0\xc7 \xc6\xf7\xbd\xba\xc6\xae\xb7\xce \xb3\xaa\xb4\xa9\xbe\xee \xc6\xf7\xbd\xba\xc6\xc3 \xb5\xcb\xb4\xcf\xb4\xd9.')

        self.staticLine1 = wx.StaticLine(id=wxID_OPTIONDIALOGSTATICLINE1,
              name='staticLine1', parent=self, pos=wx.Point(8, 472),
              size=wx.Size(384, 1), style=0)

        self.staticText1 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT1,
              label='\xc1\xd6\xbc\xd2', name='staticText1', parent=self,
              pos=wx.Point(16, 32), size=wx.Size(40, 14), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_OPTIONDIALOGSTATICBOX1,
              label='BLOG API \xbc\xb3\xc1\xa4', name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(384, 88), style=0)
        self.staticBox1.SetToolTipString('')

        self.staticText2 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT2,
              label='\xbb\xe7\xbf\xeb\xc0\xda ID', name='staticText2',
              parent=self, pos=wx.Point(208, 64), size=wx.Size(52, 14),
              style=0)

        self.staticText13 = wx.StaticText(id=wxID_OPTIONDIALOGSTATICTEXT13,
              label='Blog ID', name='staticText13', parent=self,
              pos=wx.Point(16, 64), size=wx.Size(42, 14), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.config = parent.config
        self.parent = parent
        
        
        




    ##################################################################
    ################## 대화 상자 이벤트 관련 #########################

    def OnOkBtnButton(self, event):
        """ 현재 대화상자의 내용을 parent의 config에 저장함 """
        
        self.config.blogAPI["address"] = self.blogAPIAddressTxt.GetValue()
        self.config.blogAPI["ID"] = self.blogAPIIdTxt.GetValue()
        self.config.blogAPI["userID"] = self.blogAPIUserIDtxt.GetValue()
        
        self.config.maxItemCount = self.maxItemCntSpin.GetValue()
        
        self.config.categoryName = self.categoryNameTxt.GetValue()
        
        self.config.viewPolicy["비공개"] = self.nonpublicPolicyCmbbox.GetValue()
        self.config.viewPolicy["전체공개"] = self.publicPolicyCmbbox.GetValue()
        self.config.viewPolicy["일촌공개"] = self.restrictedpublicPolicyCmbbox.GetValue()
        
        self.config.getComments = self.getCommentsChkbox.GetValue()
        
        self.config.doSyncDate = self.doSyncDateChkbox.GetValue()
        
        event.Skip()
        


    def OnCancelBtnButton(self, event):
        event.Skip()



    def OnOptionDialogInitDialog(self, event):
        """ parent의 config 객체를 이용해서 대화상자 초기화 """
        import os
        
        self.blogAPIAddressTxt.SetValue(self.config.blogAPI["address"])
        self.blogAPIIdTxt.SetValue(self.config.blogAPI["ID"])
        self.blogAPIUserIDtxt.SetValue(self.config.blogAPI["userID"])
        
        self.maxItemCntSpin.SetValue(self.config.maxItemCount)
        
        self.categoryNameTxt.SetValue(self.config.categoryName)
        
        self.nonpublicPolicyCmbbox.SetValue(self.config.viewPolicy["비공개"])
        self.publicPolicyCmbbox.SetValue(self.config.viewPolicy["전체공개"])
        self.restrictedpublicPolicyCmbbox.SetValue(self.config.viewPolicy["일촌공개"])
        
        self.getCommentsChkbox.SetValue(self.config.getComments)
        self.doSyncDateChkbox.SetValue(self.config.doSyncDate)
        
        
        #################################################################################
        # debug 설정
        if self.parent.debug:
            print "optionDlg.init()"
            self.blogAPIAddressTxt.SetValue(os.environ["BLOG_API_URL_TISTORY"])
            self.blogAPIIdTxt.SetValue(os.environ["BLOG_API_ID_TISTORY"])
            self.blogAPIUserIDtxt.SetValue(os.environ["BLOG_API_USER_ID_TISTORY"])

        #################################################################################
        
        
        event.Skip()
        
        

    def OnOptionDialogClose(self, event):
        event.Skip()
        

        















