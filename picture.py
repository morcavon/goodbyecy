# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        picture.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/03/27
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------


import re, time
import datetime

class Picture:
    """ ����ø �Խù� �ϳ��� ���� ������..."""
    
    
    def __init__(self):
        
        self.category = "�����̸�"
        self.title = "�������"
        self.createTime = None
        self.policy = "�����"
        self.tag = []
        self.Comments = []
        self.filename = ""
        self.data = ""
        self.content = ""
        self.pageNo = 0           # �� �Խù��� �ش� ������ ���° �������� �ִ��� ���
        
        
        
    def __str__(self):
        retValue = """
        << %s >>
category   : %s
create date: %s
open policy: %s
tag        : %s
comments   :
%s
filename   : %s
filessize  : %d
"""  % (self.title, self.category, datetime.datetime.strftime(self.createTime, "%Y.%m.%d %H:%M") if self.createTime != None else "", self.policy, ", ".join(self.tag), "\n".join(self.Comments), self.filename, len(self.data))
        
        return retValue
    
    
    @staticmethod
    def getTotalCount(folderList):
        """ folderList�� �ִ� ����ø �����鿡 �ִ� �� �Խù� �� ����"""
        total = 0
        
        for folder in folderList:
            total += int(folder["count"])
            
        return total
            
          
          
          
          
    @staticmethod
    def getInstance(htmlSrc, doSyncDate=True, getComments=True, categoryName="", pageno=0):
        
#        htmlSrc = re.compile("""<span class="title-text-wrap">(.+)����Է���""", re.DOTALL).findall(htmlSrc)[0]      # �ʿ���� �κ��� ����������
        retValue = Picture()

        try:
            retValue.content = re.compile("""name="brd_content_.+?>(.+?)</span>""", re.DOTALL | re.IGNORECASE).findall(htmlSrc)[0]
        except:
            retValue.content = ""
        
        retValue.category = categoryName
        retValue.title = re.compile("""title-text-wrap">(.+?)</span""").findall(htmlSrc)[0]
        
        
        temp = re.compile("""(\d+)\.(\d+)\.(\d+) (\d+):(\d+)""").findall(htmlSrc)[0]
        temp = map(lambda x: int(x), temp)
        retValue.createTime = datetime.datetime(temp[0], temp[1], temp[2], temp[3], temp[4])
            
            
            
        retValue.policy = re.compile("""bopenText0">(.+?)</span>""", re.DOTALL).findall(htmlSrc)[0].strip()
        
        temp = ""
        # tag�� ���� ��쿡�� ����
        try:
            temp = re.compile("""tag" value="(.+?)\"""", re.DOTALL).findall(htmlSrc)[0].split()
        except:
            pass
        
        for idx in range(len(temp)):
            if idx % 2 == 1 and ("<input" not in temp[idx]):
                retValue.tag.append(temp[idx])
                
        if getComments:
            temp = re.compile("""sname01">(.+?)</a.+?comment.+?">(.+?)</span>.+?'date'>\((.+?)\)""", re.DOTALL).findall(htmlSrc)
            for el in temp:
                retValue.Comments.append("    ".join(el))
        

        
        retValue.pageNo = pageno
        
        
        return retValue








