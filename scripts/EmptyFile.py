import os

def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024)
    return round(fsize,2)

def EmptyFile(InputPath, OutputText):
    EmptyFile = {}
    for i in os.listdir(InputPath):
        EmptyFile[i] = []
        if os.path.isdir("%s/%s"%(InputPath,i)):
            for ifile in [ ifile for ifile in os.listdir("%s/%s"%(InputPath,i)) if (get_FileSize("%s/%s/%s"%(InputPath,i,ifile)) < 1) & (".root" in ifile) ] :
                EmptyFile[i].append("%s/%s/%s"%(InputPath,i,ifile))
        print "finish",i
    with open(OutputText,"w") as f:
        f.write(str(EmptyFile))

def StatInfo(OutputText):
    with open(OutputText,"r") as f:
        exec('EmptyFile = '+f.read())
        count = 0
        for i in EmptyFile:
            for j in EmptyFile[i]:
                count += 1
        return count,EmptyFile



InputPathNtuple = "/stash/user/qilongguo/public/gKK/Ntuple/2016/V1/"
OutputText = "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/Temp/EmptyFile/Ntuple.txt"
# EmptyFile(InputPath, OutputText)
_,EmptyNtuple = StatInfo(OutputText) # 5837, 14480

InputPathNano = "/stash/user/qilongguo/public/gKK/private_NanoAOD/V1/"
OutputText = "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/Temp/EmptyFile/CustNano.txt"
# EmptyFile(InputPath, OutputText)
_,EmptyNano = StatInfo(OutputText) # 993 , 14766
EmptyNano_list = []
for i in EmptyNano:
    EmptyNano_list += EmptyNano[i]

count = 0
printN = 10
for i in EmptyNtuple:
    for j in EmptyNtuple[i]:
        CorrespondingNano = "%s/%s/%s"%(InputPathNano,j.split("/")[-2],j.split("/")[-1])
        if CorrespondingNano not in EmptyNano_list:
            if get_FileSize(CorrespondingNano) > 1000:
                count += 1
print count