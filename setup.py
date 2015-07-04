# _*_ coding: mbcs _*_
from distutils.core import setup
import py2exe
import sys, time, re, os, shutil

if os.path.exists("GoodbyeCy.py") and not os.path.exists("GoodbyeCy.pyw"):
    os.rename("GoodbyeCy.py", "GoodbyeCy.pyw")


# versioning
buildNum = int(open("build.txt", "r").read())
buildNum = str(buildNum + 1)
open("build.txt", "w").write(buildNum)




# 소스를 수정하여 빌드 넘버를 안에다 삽입 (mainFrame.py)
rex = """# Version:[ ]+([^ \n]+)"""

srcIn = open("mainFrame.py","r")
srcString = srcIn.read()
srcIn.close()

version = re.compile(rex).findall(srcString)[0].split(".")
version[2] = buildNum
newVersion = ".".join(version)

newSrc = re.sub(rex, "# Version:     " + newVersion, srcString, 1)
newSrc = re.sub("version =.+\n", """version = \"%s\"\n""" % newVersion, newSrc, 1)

open("mainFrame.py", "w").write(newSrc)




appName = "GoodbyeCy"

if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.3." + buildNum
        self.company_name = "http://www.morcavon.com"
        self.copyright = "morcavon"
        self.name = appName.decode('mbcs')

################################################################
# A program using wxPython

# The manifest will be inserted as resource into test_wx.exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store it in a file named
# test_wx.exe.manifest, and copy it with the data_files option into
# the dist-dir.
#
manifest_template = '''
<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<assembly xmlns='urn:schemas-microsoft-com:asm.v1' manifestVersion='1.0'>
 <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
  <security>
   <requestedPrivileges>
    <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
   </requestedPrivileges>
  </security>
 </trustInfo>
</assembly>
'''

RT_MANIFEST = 24

app = Target(
    # used for the versioninfo resource
    description = "Cy 사진첩을 Blog API를 지원하는 블로그로 이동".decode('mbcs'),

    # what to build
    script = "%s.pyw" % appName,
##    other_resources = [(RT_MANIFEST, 1, manifest_template)],
    icon_resources = [(1, "icon.ico")],
    )

################################################################
from glob import glob
setup(
    options = {"py2exe": {
                          "compressed": 1,
                          "optimize": 2,
                          "dist_dir":appName,
                          "bundle_files": 1,
                          "packages":["spynner","cookielib"],
						  "includes":"sip",
                          }},
    zipfile = None,
    windows = [app],
	#data_files=[("javascript", glob(r"javascript\*.js"))],
    )




# clean up
shutil.rmtree(os.path.join(os.getcwd(), "build"))

