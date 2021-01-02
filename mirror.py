import ftplib
from ftplib import FTP
import os
import datetime

#ftp login details
HOST = ''
USERNAME = ''
PASSWORD = ''
FTPDIR = ''

#pomocne funkcie
def changeDir(osdir, ftpdir):
    ftp.cwd(ftpdir)
    os.chdir(osdir)

def upFileBinary(fname):
    with open(fname, 'rb') as f:
        ftp.storbinary('STOR %s' % fname, f)
    print('file ' + fname + ' uploaded')

#core funkcie
def uploadFile(fname):
    ftppath = ftp.pwd()
    ospath = os.getcwd()

    #zisti ci uz nahodou file nie je na serveri
    if fname in ftp.nlst():
        file_disk_size = os.path.getsize(ospath + '\\' + fname)
        file_ftp_size = ftp.size(ftppath + '/' + fname)

        #zisti ci sa velkosti nerovnaju
        if file_disk_size == file_ftp_size:
            print('file ' + fname + ' of the same size already exists')
        else:
            upFileBinary(fname)
    else:
        upFileBinary(fname)

def checkDir(ospath, ftppath):
    #iteruj zoznam fileov a foldrov
    for item in os.listdir(ospath): 

        #zisti ci je polozka file alebo folder
        if str(item).find(".") == -1: 
            #print(ftp.nlst())

            #zisti ci folder existuje na ftp, ak ano potrebujeme rekurzivne iterovat obsah priecinka
            if str(item) in ftp.nlst(): 
                print('folder ' + item + ' exists')
                #zmen priecinok na disku aj serveri
                changeDir(item, item)
                #rekurzivne volanie
                checkDir(os.getcwd(), ftp.pwd())
                #vratit naspat cwd pre pc aj server
                changeDir(ospath, ftppath)
            else:
                #folder neexistuje tak ho vytvorim
                ftp.mkd(item)
                print('folder ' + item + ' created')
                #zmen priecinok na disku aj serveri na novy folder
                changeDir(item, item)
                #rekurzivne volanie
                checkDir(os.getcwd(), ftp.pwd())
                #vratit naspat cwd pre pc aj server
                changeDir(ospath, ftppath)

        #ak je to file
        else:
            uploadFile(item)

#scandir(os.getcwd())
ftp = FTP(HOST, USERNAME, PASSWORD)
print ("Welcome: ", ftp.getwelcome())
ftp.cwd(FTPDIR)

osdir = os.getcwd()
ftpdir = ftp.pwd()

checkDir(osdir, ftpdir)

ftp.close()


