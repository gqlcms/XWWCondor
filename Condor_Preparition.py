import os

def PrivateSamples_List(Path,configPath):
    for i in os.listdir(Path):
        if os.path.isdir("%s/%s"%(Path,i)):
            with open("%s/%s.txt"%(configPath,i),"w") as f:
                for ifile in os.listdir("%s/%s"%(Path,i)):
                    if ".root" in ifile:
                        f.write(ifile+"\n")

Path = "/stash/user/qilongguo/public/gKK/private_NanoAOD/V1/"
configPath = "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/samples/Cust_Nano2016_v9"
PrivateSamples_List(Path,configPath)