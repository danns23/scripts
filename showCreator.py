#!/usr/bin/env python

# This script will take a wav file in the format of xxxx_####-MM-DD-YY.wav where:
#   xxxxx - Is the show name
#   #### - Is the show number
#   MM - Month
#   DD - Day
#   YY - Year (can be more than 2 or 4 digits)
#
#  Additional options are passed in use -h for parameters:
#
#  -f, --filename - The wav file name in the format described above
#  -t, --title - Title of the show to appear in the audio file tags.
#  -a, --artists - List of artists to appear in the audio file tags.
#  -d, --date - Date of the show to appear in the audio file tags
#  -n, --name - Name of the show to appear in the audio file tags.
#
#  If you want to use the ftp fuction set the ftpUsername, ftpPassword, and ftpDirectory accordingly and set uploadFiles = True.
# 
#  Choose what audio formats you want to encode below.

import sys
import os
import subprocess
import datetime
from optparse import OptionParser
from ftplib import FTP

uploadFiles= False
ftpUsername = ''
ftpPassword = ''
ftpDirectory = ''

today = datetime.date.today()

doOgg = True 
doSpx = True
doOpus = True
doMp3 = True
PARSER = OptionParser()
PARSER.add_option("-f", "--filename", dest="filename", default="",
                  help="The name of the sound file to process")
PARSER.add_option("-t", "--title", dest="title", default="Super Awesome Show", help="The title of the show or guests")
PARSER.add_option("-a", "--artists", dest="artists", default="allan, dann, pat, linc", help="artists on the show")
PARSER.add_option("-d", "--date", dest="date", default=today.strftime("%m-%d-%Y"), help="date the show was put together")
PARSER.add_option("-n", "--name", dest="name", default="TLLTS", help="Name of the show abbreviation")
(OPTIONS, ARGS) = PARSER.parse_args()
FILENAME = OPTIONS.filename
TITLE = OPTIONS.title
ARTISTS = OPTIONS.artists
NAME = OPTIONS.name
HOME = os.environ['HOME']

if not os.path.exists(FILENAME):
        sys.exit("file does not exist")

fileName = FILENAME.split('.')



outPutFileBase = fileName[0]

fileNameSplit1 = fileName[0].split('_')
fileNameSplit2 = fileNameSplit1[1].split('-')
showNumber = fileNameSplit2[0]


SOURCEFILE = os.path.abspath(os.path.join(HOME, FILENAME))

def encodeOgg(oggFileName):
    oggEncoding = ["oggenc",
                    "-q",
                    "3",
                    "-a",
                    ARTISTS,
                    "-t",
                    "tllts-%s: %s" % (showNumber,TITLE),
                    "-G",
                    "Podcast",
            "-l", 
            NAME,
                    "-o",
                    "%s" % oggFileName,
                    "%s" % FILENAME]

    print ("oggEncoding")
    print ("\n")

    subprocess.Popen(oggEncoding).communicate()

def encodeSpx(spxFileName):
    speexEncoding = ["speexenc", 
                    "-V",
                    "--author",
                    ARTISTS,
                    "--title",
                    "tllts-%s: %s" %(showNumber,TITLE),
                    "%s" % FILENAME,
                    "%s" % spxFileName]

    print ("speexEncoding")
    print ("\n")

    subprocess.Popen(speexEncoding).communicate()


def encodeMp3(mp3FileName):
    mp3Encoding = ["lame",
                    "-b",
                    "32",
                    "-q",
                    "1",
                    "--tt",
                    "tllts-%s: %s" % (showNumber,TITLE),
                    "--ta",
                    ARTISTS,
                    "--ty",
                    "2010",
                    "--tg",
                    "Speech",
                    "--tl",
            NAME,
                    "%s" % FILENAME,
                    "%s" % mp3FileName]

    print ("mp3Encoding")
    subprocess.Popen(mp3Encoding).communicate()

def encodeOpus(opusFileName):
    opusEncoding = ["opusenc",
                    "--bitrate",
                    "32",
                    "--title",
                    "tllts-%s: %s" %(showNumber,TITLE),
                    "%s" % FILENAME,
                    "%s" % opusFileName]
    print ("opusEncoding")
    subprocess.Popen(opusEncoding).communicate()


def ftpFiles(fileList, ftpUsername, ftpPassword, ftpDirectory=None):
    ftp = FTP('tlltsarchive.org')
    ftp.login(ftpUsername, ftpPassword)
    if ftpDirectory != None:
        ftp.cwd(ftpDirectory)

    for uploadFile in fileList:
        print ("opening %s \n" % uploadFile)
        fileUp = open(uploadFile, 'rb')
        ftp.storbinary("STOR " + uploadFile,fileUp,8192) 
        fileUp.close()

    ftp.close()


def encodeFiles(outPutFileBase):
    print "encoding files"
    fileList = []
    if doOgg: 
        oggFileName = outPutFileBase + '.ogg'
        encodeOgg(oggFileName)
        fileList.append(oggFileName)

    if doSpx:
        spxFileName = outPutFileBase + '.spx'
        encodeSpx(spxFileName)
        fileList.append(spxFileName)

    if doOpus:
        opusFileName = outPutFileBase + '.opus'
        encodeOpus(opusFileName)
        fileList.append(opusFileName)

    if doMp3:
        mp3FileName = outPutFileBase + '.mp3'
        encodeMp3(mp3FileName)
        fileList.append(mp3FileName)

    return fileList

if __name__ == "__main__":
    fileList = encodeFiles(outPutFileBase)
    if uploadFiles:
        ftpFiles(fileList, ftpUsername, ftpPassword, ftpDirectory)

