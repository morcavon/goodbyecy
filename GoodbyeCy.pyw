# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        GoodbyCy.pyw
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/27
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------
#!/usr/bin/env python
#Boa:App:BoaApp

import wx
import mainFrame

#import psyco
#psyco.full()
#psyco.profile(0.0)

modules ={'mainFrame': [1, 'Main frame of Application', 'mainFrame.py'],
 u'optionDlg': [1, 'Option Dialog frame', u'optionDlg.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = mainFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
