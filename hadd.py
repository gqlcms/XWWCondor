import os
import ROOT as r

def get_FileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024)
    return round(fsize,2)

def Check_BadFiles(file,TreeName = "Events"):
    foundBad = False
    try:
        f1 = r.TFile(file)
        t = f1.Get("t")
        nevts = t.GetEntries()
        for i in range(0,t.GetEntries(),1):
            if t.GetEntry(i) < 0:
                foundBad = True
                print "[RSR] found bad event %i" % i
                break
    except: foundBad = True
    return foundBad

def hadd_Tree(InputPath, OutputPath, ScriptsPath, py = "haddnano.py"):
    for i in os.listdir(InputPath):
        print i
        if os.path.isdir("%s/%s"%(InputPath,i)):
            with open("%s/%s.sh"%(ScriptsPath,i),"w") as f:
                files = ""
                for ifile in [ ifile for ifile in os.listdir("%s/%s"%(InputPath,i)) if (".root" in ifile) & (get_FileSize("%s/%s/%s"%(InputPath,i,ifile)) > 1)] :
                    files += "%s/%s/%s "%(InputPath,i,ifile)
                if ".root" in files:
                    hadd = '%s %s/%s.root %s >%s/%s.debug 2>&1 &\n'%( py, OutputPath, i, files, ScriptsPath, i )
                    f.write(hadd)

InputPath = "/stash/user/qilongguo/public/gKK/Ntuple/2016/V1/"
OutputPath = "/stash/user/qilongguo/public/gKK/Tree/2016/V1/"
ScriptsPath = "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/WrongBranches/"
hadd_Tree(InputPath, OutputPath, ScriptsPath, py = "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/scripts/FileWithdifferent_Branches.py")