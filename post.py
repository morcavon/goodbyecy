# _*_ coding: mbcs _*_
#-----------------------------------------------------------------------------
# Name:        post.py
# Author:      morcavon
# Email:       morcavon@gmail.com
# Homepage:    http://www.morcavon.com
# Created:     2009/04/29
# Copyright:   Copyright (c) morcavon. All rights reserved.
# Licence:     Freeware, see license.txt for details(if any :-))
#-----------------------------------------------------------------------------


class Post():
    """ 블로그에 올릴 포스트 하나를 나타내는 클래스... """
    
    def __init__(self, server, pictures, config, blogPassword, debug=False):
        self.server = server
        self.pictures = pictures
        self.config = config
        self.blogPassword = blogPassword
        self.fileURLs = []
        self.category = pictures[0].category
        self.debug = debug
        
        self.logFile = open("goodbyeCy.log", "a")
        
        
        # blog type 구별
        if "rpc.egloos.com" in self.config.blogAPI["address"]:
            self.blogType = "egloos"
        elif "textcube.com" in self.config.blogAPI["address"]:
            self.blogType = "textcube"
        elif "cyhome.cyworld.com" in self.config.blogAPI["address"]:
            self.blogType = "cyworld"
        else:
            self.blogType = "tistory"
            
            
        # 몇가지 처리...
        if self.blogType == "cyworld":
            self.config.blogAPI["userID"] = self.config.blogAPI["ID"]
        
       
        self.contents = self.generateHTML()
        
        
        
        
    def checkFileDup(self, pictureList):
        """ 한 포스트에 같은 파일명이 존재하면 제대로 업로드가 되지 않으므로 중복된 파일은 적절하게 파일명 변경 """
        
        import os
        
        for idx, picture in enumerate(pictureList):
                
            for dupidx, duppicture in enumerate(pictureList[idx+1:]):
                if duppicture.filename == picture.filename:
                    pictureList[idx+1+dupidx].filename = "%s_%d%s" % (os.path.splitext(picture.filename)[0], dupidx, os.path.splitext(picture.filename)[1])
        
        
        return pictureList        
        
        
    def generateHTML(self):
        """ pictures를 이용하여 포스트 본문을 생성하고, 그 과정에서 구한 파일 url을 따로 저장 """
        
        import time
        import datetime
        
        retValue = ""
        data = {}
        
        pictureTemplate = """<div class="article">
 <strong><span style="font-size: 11pt;"><span style="font-family: Dotum;"><font color="#000000">
<div style="border: 1px dashed rgb(193, 193, 193); padding: 10px; background-color: rgb(243, 244, 235);" class="txc-textbox">
<div style="text-align: center;">
<strong><span style="font-size: 11pt;"><span style="font-family: Dotum;"><font color="#000000">%(title)s</font></span></span></strong><br />
</div>
</div>
</font></span></span></strong></div>
<div style="text-align: right;">
<div>
<strong><span style="font-size: 11pt;"><span style="font-family: Dotum;"></span></span></strong><font color="#000000">%(date)s<br />
</font></div>
</div>
<div>
<div>
<br />
&nbsp;</div>
</div>
%(imageURL)s
<br />
<br />%(body)s
<br />
<br />
<br />
<font color="#000000"><span style="font-family: Gulim;"><strong>태그&nbsp;&nbsp;&nbsp;&nbsp;</strong></span></font>%(tags)s<br />
<br />
<br />

<div style="border: 1px none rgb(219, 232, 251); padding: 10px; background-color: rgb(232, 240, 247);" class="txc-textbox">
<font color="#000000">%(comments)s</font></div>
<br />


<hr style="border: 0pt none ; position: relative; top: -999px; left: -999px;">
"""

        self.pictures = self.checkFileDup(self.pictures)
        
        for picture in self.pictures:
            data["title"] = picture.title
            data["date"] = datetime.datetime.strftime(picture.createTime, "%Y.%m.%d %H:%M")
            data["imageURL"] = self.getImageURL(picture)
            data["body"] = picture.content
            data["tags"] = ", ".join(picture.tag)
            data["comments"] = self.decorateComments(picture.Comments) if self.config.getComments else ""
            
            retValue += pictureTemplate % data
            
        
        return retValue
        
        
        
    def upload(self, debug=False):
        """ 실제 업로드가 수행되는 부분...."""
        
        import xmlrpclib
        import datetime
        
        struct = {}
        struct["title"] = self.pictures[0].title
        struct["categories"] = ["%s/%s" % (self.config.categoryName, self.pictures[0].category),]
        struct["description"] = self.contents.replace("\r\n", "<br>")
        struct["dateCreated"] = (self.pictures[0].createTime if self.config.doSyncDate else datetime.datetime.today()) - datetime.timedelta(1.0/24*9)

        newPolicy = self.config.viewPolicy[self.pictures[0].policy]
        
        
        # xml 로 보낼때는 ut8로 바꿔야 하는뎅....
        for key, value in struct.items():
            
            try:
                if key == "dateCreated":
                    continue
                
                if key == "categories":
                    struct[key] = map(lambda x: unicode(x.decode("cp949")), value)
                    
                else:
                    struct[key] = unicode(value.decode("cp949"))
            except:
                if debug:
                    print "upload.unicode conversion error=>>>", key, value
            
            
        try:
            self.server.metaWeblog.newPost(self.config.blogAPI["ID"], self.config.blogAPI["userID"], self.blogPassword, struct, True if newPolicy == "공개" else False)
        except Exception, msg:
            if debug:  
                print "post.upload: posting failed", msg
            
            
            tempStr = """[포스팅 실패]
%s

"""
            for el in self.pictures:
                self.logFile.write(tempStr % el)
                
                
            # TOO MANY POSTING exception (TISTORY)
            if "Fault 5" in str(msg):
                return 5
            
            if "Invalid Login" in str(msg):
                return 101
                
                
        
        
        ################# 이 부분이 필요할라나??? ###########################
        # TISTORY
        if "tistory.com" in self.config.blogAPI["address"]:
            pass
        else:
            # 티스토리 이외의 블로그는 차후 구현...
            pass
        
        
        return 0



        

    def getImageURL(self, picture):
        """ picture의 파일 데이터를 업로드하고 url를 포함한 태그 코드를 리턴함, 블로그 별로 url 형식이 다르므로 구별해야 함... """
        import xmlrpclib, os
        
        
        
        retURL = ""
        struct = {}
        struct["name"] = unicode(picture.filename.decode("cp949"))
        struct["bits"] = xmlrpclib.Binary(picture.data)
        struct["type"] = "image/jpeg" if os.path.splitext(picture.filename)[1] in (".jpg", ".jpeg", ".gif", ".png") else "application/x-shockwave-flash"
        
        
        # 이글루는 타입을 이미지로 
        if self.blogType == "egloos":
            struct["type"] = "image/jpeg"
        
        
        try:
            
            ext = os.path.splitext(picture.filename)[1].lower()
            
            
            if self.blogType in ("egloos", "cyworld") and ext == ".swf":
                return "현재 블로그는 플래시 파일 업로드를 지원하지 않습니다."
            
            
            retURL = self.server.metaWeblog.newMediaObject(self.config.blogAPI["ID"], self.config.blogAPI["userID"], self.blogPassword, struct)["url"]
            
            
            ################################################################
            if self.blogType == "tistory":
                retURL = retURL + "&filename=" + retURL.split("/")[-1]
#                if self.debug:   print "post.getImageUrl.mediaURL: ", retURL
            ################################################################
                
        
            
           
            if ext in (".jpg", ".gif", ".jpeg", ".png"):
 
                
                ################################################################
                if self.blogType == "tistory":
                    retURL = """[##_1C|%s|width="400" alt="" filename="%s" filemime=""|_##]""" % (retURL.split("filename=")[-1], retURL.split("filename=")[-1])
                elif self.blogType in ("egloos", "cyworld"):
                    retURL = """<img src="%s" width="400" """ % retURL
                elif self.blogType == "textcube":
                    retURL = """<ttml tt_class="fileone" tt_w="400px" tt_alt="" tt_link="" tt_filename="%s" tt_caption="" tt_align="center" tt_type="img" />""" % retURL
                ################################################################
                
                
                
            elif ext.lower() == ".swf":
                if self.blogType == "textcube":
                    retURL = """<ttml tt_class="object" tt_w="400px" tt_h="800px" tt_align="center"><object height="800" width="400" data="%(filename)s" type="application/x-shockwave-flash"><param value="%(filename)s" name="movie" /></object></ttml>""" % {"filename": retURL.split("filename=")[-1]}
                
                else:
                    retURL = """<DIV style="TEXT-ALIGN: center"><embed width="400" height="800" src="/attachment/%s" autoplay="true" quality="high" allowScriptAccess="always" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/><br />
    </DIV>""" % retURL.split("filename=")[-1]
    
    
#            if self.debug:   print "post.getImageUrl.info:", self.blogType, ext, retURL
    
    
        except Exception, msg:
##            print msg
            
            self.logFile.write("""[첨부파일 업로드 실패]
폴더명: %s
제목: %s
파일명: %s

""" % (picture.category, picture.title, picture.filename))

            return "%s 파일 업로드중 오류가 발생하였습니다." % picture.filename
        
        
        return retURL
    
    
    def decorateComments(self, comments):
        """ 코멘트를 이쁘게(?) 꾸며서 리턴... """
        retValue = ""
        for comment in comments:
            tempStr = comment.split(" ", 1)
            retValue += "<b>%s:</b> %s<br />\n" % (tempStr[0], tempStr[1])
    
    
        return retValue
    
    
    
    
    def __str__(self):
        
        retValue = """
    [[ %s ]]
# of pictures : %d
""" % (self.pictures[0].category, len(self.pictures))
    

        return retValue
    






if __name__ == "__main__":
    import xmlrpclib
    import os
    from datetime import datetime
    
    try:
        os.remove("d:/a.xml")
    except:
        pass

    serverURL = "http://cyhome.cyworld.com/a0404791/api"
    blogID = "a0404791"
    userID = "a0404791"
    password = "4b16131f9269c"
    
    server =  xmlrpclib.Server(serverURL)
    
#    print dir(server)
#    print server.metaWeblog.newPost()
#    exit(0)
        
    # getPost
    
##    res = server.metaWeblog.getPost("68978-1", userID, password)
##    print res
##    exit(0)
    ############################
    
    
    

    struct = {}
    struct["name"] = "test.jpg"
#    struct["type"] = "image/jpeg"
    struct["type"] = "application/x-shockwave-flash"
    struct["bits"] = xmlrpclib.Binary(open("d:/test.swf", "rb").read())
#    struct["bits"] = xmlrpclib.Binary(open("d:/test.jpg", "rb").read())

    
    url = server.metaWeblog.newMediaObject(blogID, userID, password, struct)['url']
#    url = url + "&filename=" + url.split("/")[-1]
    
    print url
#    exit(0)
    
    ##################################
    #  unicode(value.decode("cp949"))
    struct = {}
    struct["title"] = "test title하이"
#    struct["categories"] = []
##    struct["description"] = """zxczxcbxzb<br><img src="[##_ATTACH_PATH_##]/%s" /><br>zxcbzxbcx""" % url.split("filename=")[-1]  # for jpg
##    struct["description"] = """zxczxcbxzb<br><embed width="400" height="800" src="/attachment/%s" quality="high" allowScriptAccess="always" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer"/><br>zxcbzxbcx""" % url.split("filename=")[-1]      # for swf
    struct["description"] = 'hello 이건뭐야world <img src="%s"' % url
##    struct["dateCreated"] = datetime(2005,1,1,10-9,10)
    
    
    for key, value in struct.items():
            
            try:
                if key == "dateCreated":
                    continue
                
                if key == "categories":
                    struct[key] = map(lambda x: unicode(x.decode("cp949")), value)
                    
                else:
                    struct[key] = unicode(value.decode("cp949"))
#                    struct[key] = value.decode("utf8")
            except:
                print "upload.unicode conversion error=>>>", key, value
    
    print str(struct)
    
    print server.metaWeblog.newPost(blogID, userID, password, struct, False)
    
    
    
    
    
    
    
    
    
    
    










