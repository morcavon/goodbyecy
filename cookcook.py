# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        cookcook.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/11/21
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------


import sys,traceback, os, urllib
import spynner
from StringIO import StringIO

debug_stream = StringIO()
def run_debug(callback, *args, **kwargs): # ** *
    pos = debug_stream.pos
    ret = callback(*args, **kwargs)
    show_debug(pos)
    return ret


def show_debug(pos=None):
    if not pos: print debug_stream.getvalue()
    else:
        pnow = debug_stream.pos
        debug_stream.seek(pos)
        print debug_stream.read()
        debug_stream.seek(pnow)


class CookCook:
    def __init__(self, email, passwd, debug):
        self.email = email
        self.passwd = passwd
        self.debug = debug

        self.cookie = ""        # 로그인후의 쿠기 저장
        self.tid = ""
        self.cookie_photo =""      # 사진첩게시판로딩후 쿠기
        self.errmsg = ""
    
        self.PAGE_LOAD_WAIT_TIME = 3
        
 

    def getTidFromCookie(self, cookie):
        import re
        
        retVal = ["",]
        
        if "CFN=" in cookie:
            retVal = re.compile("""&id=(\d+)""").findall(cookie)
            if len(retVal) <= 0:
                retVal = re.compile("""NickID=(\d+)""").findall(cookie)
                if len(retVal) <= 0:
                    retVal = ["",]
                    
        return retVal[0] 
        

    def getCookie(self):
        from time import sleep
        import re

        self.errmsg = ""
        tid = ""
        self.cookie = ""
        self.cookie_photo = ""
		
        browser = spynner.Browser(debug_level=spynner.DEBUG, debug_stream=debug_stream)
       
        try:
			########  로그인 하자~~~            
            browser.load("http://www.cyworld.com/cymain/?f=cymain")
            browser.load_jquery(force=True)
            browser.fill('input[name="ID"]', self.email)
            browser.fill('input[name="PASSWD"]', self.passwd)
            
            if self.debug:  open("beforeClick.html","w").write(browser.html.encode("mbcs"))
            browser.click("input[name=btnLOGIN]")
            browser.wait(self.PAGE_LOAD_WAIT_TIME)
            
            if self.debug:  open("afterLogin.html","w").write(browser.html.encode("mbcs"))
				
            # 로그인 실패 여부 체크
            if self.email not in browser.html:
            	self.errmsg = "이메일 혹은 비밀번호가 일치하지 않습니다. 다시 확인해 주세요."
            	return
            elif self.debug:
            	print "cookcook.getCookie: 이메일/비번 오류없음"
            
            c = browser.get_cookies()
            self.tid = self.getTidFromCookie(c)
            if self.debug:  open("cookie.txt", "w").write(c)
            
            #===============================================================
            #self.tid = "21251087"
            #===============================================================

            # 사진첩 게시판 로딩후 쿠기 얻기
            browser.load("http://minihp.cyworld.com/svcs/MiniHp.cy/index/%s?tid=%s&urlstr=phot" % (self.tid, self.tid))
            browser.wait(self.PAGE_LOAD_WAIT_TIME)
            c = browser.get_cookies()
            self.cookie_photo = self.make_cookie_photo(c)
            if self.debug:	open("cookie_photo.txt", "w").write(self.cookie_photo)
            
            
        except Exception, msg:
            if self.debug:
                print "Exception: ", msg
                traceback.print_exc(file=sys.stdout)
            self.errmsg = "로그인에 문제가 있습니다. 인터넷 연결 상태 및 로그인 이메일과 비밀번호를 다시 확인하세요...."
            return


        finally:
            if self.debug:  print "cookcooke.getCookie: in finally"
            
			
			


    def setCookie(self, headers):
        import re

        if self.debug:  open("cookie_before", "w").write(self.cookie_photo)

        for header in headers:
            if header[0] == "set-cookie":
                for cookie in header[1].split(","):
                    cookie = cookie.split(";")[0]

                    # 없으면 추가하고, 기존에 있는거면 덮어써...
                    rex = """(%s\=.+?);""" % cookie.split("=", 1)[0]
                    self.cookie_photo = re.sub(rex, cookie + ";", self.cookie_photo)

        if self.debug:  open("cookie_after", "w").write(self.cookie_photo)





    def getPage(self, url,  cookie_select, referer="", method="GET", host="minihp.cyworld.com", language="ko-KR", charset="",
                accept="""application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*"""):
        # return uncompressed page contents

        import gzip
        import StringIO
        import httplib


        h = httplib.HTTPConnection(host)
        h.putrequest(method, url, skip_accept_encoding=True, skip_host=True)
        h.putheader('Accept', accept)
        if referer != "":   h.putheader("Referer", referer)
        h.putheader("Accept-Language", language)
        h.putheader("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322)")
        h.putheader("Accept-Encoding", "gzip, deflate")
        if charset != "":   h.putheader("Accept-Charset", charset)
        h.putheader("Host", host)
        h.putheader("Connection", "Keep-Alive")
        h.putheader("Cookie", cookie_select)
        h.endheaders()
        response = h.getresponse()
        if self.debug: print response.status       # 200이면 OK

        result = response.read()
        self.setCookie(response.getheaders())
        
        try:
            gzipper = gzip.GzipFile(fileobj=StringIO.StringIO(result))
            return gzipper.read()
        except:
            return result

        
        
        
    def make_cookie_photo(self, raw_cookie):
        c = raw_cookie.replace("# Netscape HTTP Cookie File", "")
        ret = []
        
        for line in c.split("\n"):
            if len(line) <= 0:  continue
            token_list = line.split()
            #print token_list
            ret.append("%s=%s" % (token_list[5], token_list[6])) 
        
        return "; ".join(ret)
    
    
    
    
    

if __name__ == "__main__":
    obj = CookCook("morcavon@gmail.com", "", True)
    
    # make cookie_photo test
    if False:
        c = open("cookie.txt", "r").read()
        c2 = obj.make_cookie_photo(c)
        open("cookie_photo.txt", "w").write(c2)
        exit()
    
    # test
    obj.getCookie()

    referer = "http://minihp.cyworld.com/svcs/MiniHp.cy/index/%s?tid=%s&domain=&cast=&dpop=&productseq=&gift_preview=&theme=&codi=&preview_effect=&preview_effect_cd=&seq=&urlstr=&urlstrsub=&send_seq=&back=&item_seq=&act=&Nyearmon=&board_no=&choco=&product_type=&effect_menu_sel=&toyearmonday=&preview_news=&theme_seq=&theme_nm=&theme_cat=&catalog_id=&theme_from=&contents_mode=&series_num=&cinema_id=&prev_content_type=&prev_product_code=&prev_store_seq=&mana_type=&town_action=&game_store_seq=&roomsUse=&home_setting=&action=&repu_setting=&nc_refresh=" % (obj.tid, obj.tid)
    url = "/pims/main/main_inside.asp?choco=ok&dpop=&domain=&tid=%s&urlstr=&send_seq=&productseq=&home_setting=&roomsUse=&mainroom=&ml_size=&ml_menu=&ml_inst=&ml_fid=" % obj.tid
    data = obj.getPage(url, referer)


    open("data.txt", "w").write(data)









