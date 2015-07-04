# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        mainThread.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/27
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------

import os, sys
from PIL import Image
from config import Config
from picture import Picture
from threading import Thread


class MainThread(Thread):
    
    def __init__(self, parent):        
        self.parent = parent
        self.config = parent.config
        
        self.pictureList = []
        
        pass
    
    
    
    def run(self):
        while True:
            
            self.getPictures()
            self.uploadToBlog()
            
        pass
    
    
    
    
    def getPictures(self):
        """ 게시물 하나 혹은 여러개를 가져와서 리스트에 저장"""
        pass
    
    
    def uploadToBlog(self):
        """ Picture 리스트를 이용해서 포스트를 생성하고 블로그에 올림"""
        pass
    
    
    
    
    
    
    
    
    