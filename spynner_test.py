# -*- coding:mbcs -*-

import spynner

browser = spynner.Browser()
browser.load("http://www.nate.com/?f=cymain")
browser.wait(5)
c = browser.get_cookies()
open("cookies_.txt", "w").write(c)

#browser.runjs("console.log('I can run Javascript!')")
#browser.runjs("_jQuery('div').css('border', 'solid red')") # and jQuery!

#browser.select("#esen")
browser.fill("input[name=ID]", "morcavon@gmail.com")
browser.fill("input[name=PASSWD]", "")
browser.click("input[name=btnLOGIN]")
browser.wait(5)

c = browser.get_cookies()
open("cookies.txt", "w").write(c)

print browser.url, len(browser.html)
#print c
#open("a.html", "w").write( browser.html.encode("mbcs") )
#open("a.jpg", "wb").write(xxx)
#open("b.html", "w").write( browser.soup.encode("mbcs") )
open("cookies.txt", "w").write(c)

browser.close()