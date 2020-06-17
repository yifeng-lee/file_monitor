import os
import sys
import time
from shutil import copy2,move
from hashlib import sha256


def mkdir(path):
    try:
        os.mkdir(path)
    except Exception as e:
        pass


def getFileList(cwd):
    fileList = []
    for root,subdirs,files in os.walk(cwd):
        for filePath in files:
            originalfile = os.path.join(root,filePath)
            if recordStr not in originalfile:
                fileList.append(originalfile)
    return fileList

def backupFiles(fileList = []):
    for filePath in fileList:
        if recordStr not in filePath:
            copy2(filePath,record['bak'])


def getHash(filePath):   
    try:
        with open(filePath,'rb') as r:
            hash = sha256(r.read()).hexdigest()
            return hash
    except Exception as e:
       raise e


def getHashDict(fileList = []):
    fileHashDict = {}
    for filePath in fileList:
        if recordStr not in filePath:
            hash = getHash(filePath)
            if hash:
                fileHashDict[filePath] = hash
    return fileHashDict


def check(fileHashDict = {},fileList = {}):
    for filePath in fileList:  
        try:
            hash = getHash(filePath)
            if fileHashDict[filePath] != hash:
                print(fileHashDict[filePath],hash)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'文件被篡改:',filePath)
                try:
                    copy2(filePath,os.path.join(record['diff'],time.strftime("%Y-%m-%d-%H:%M:%S_", time.localtime()) + os.path.basename(filePath)))
                    copy2(os.path.join(record['bak'],os.path.basename(filePath)),filePath)
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'文件已恢复:',filePath)
                except Exception as e:
                    print('文件恢复失败:',filePath)

        except Exception as e2:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'文件被删除:',filePath)
            try:
                copy2(os.path.join(record['bak'],os.path.basename(filePath)),filePath)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'文件已恢复:',filePath)
            except Exception as e:
                pathdir = os.path.dirname(filePath)
                while not os.path.exists(pathdir):
                    mkdir(pathdir)
                    pathdir = os.path.dirname(pathdir)


def killShell(diffFileList = [],fileList = []):
    for filePath in diffFileList:
        if filePath not in fileList:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'发现疑似shell:',filePath)
            try:
                move(filePath,os.path.join(record['shell'],time.strftime("%Y-%m-%d-%H:%M:%S_", time.localtime()) + os.path.basename(filePath)))
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'shell已查杀')
            except Exception as e:
                print('shell查杀失败:',filePath)


if __name__ == "__main__":
    bak = 'bak_079fa55b870cad637d01d1580d4837ffc29c9bab' 
    shell = 'shell_ec122f54cf16a175b3e22979e240684f7734079a'
    diff = 'diff_75a0ee1ba911f2f5199177dfd31808a12511bbdc'

    cwd = os.getcwd()
    recordStr = 'record_275a700078'
    recordPath  = os.path.realpath(recordStr)
    record = {
        'bak':os.path.realpath(os.path.join(recordStr,bak)),
        'shell':os.path.realpath(os.path.join(recordStr,shell)),
        'diff':os.path.realpath(os.path.join(recordStr,diff)),
    }

    mkdir(recordPath)
    for i in record.values():
        mkdir(i)
    
    fileList = getFileList(cwd)
    backupFiles(fileList)
    fileHashDict = getHashDict(fileList)

    print('开始监控')
    while True:
        fileListNew = getFileList(cwd)
        diffFileList = list(set(fileList) ^ set(fileListNew))
        killShell(diffFileList,fileList)
        check(fileHashDict,fileList)
        time.sleep(2)