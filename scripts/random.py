import os

ScriptsPath = "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/WrongBranches/Record/"
Rerun = {}
for i in [i for i in os.listdir(ScriptsPath) if ".txt" in i]:
    with open("%s/%s"%(ScriptsPath,i),"r") as f:
        content = f.read()
        if len(content.replace(" ","").replace("\n","")) > 0:
            exec('Rerun[i.replace(".txt","")] = '+content)
            print len(Rerun[i.replace(".txt","")]),i.replace(".txt","")

