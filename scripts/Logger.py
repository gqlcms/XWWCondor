import os

class Logger:
    def __init__(self,):
        pass

    def Failedjobs_according_Output(self, log, filenames, info = lambda i:i):
        Summury = []
        with open(log,"r") as f:
            for i in f.readlines():
                for filename in filenames:
                    if filename[-10:] in i:
                        Summury.append(info(i))
        return Summury

    def LoopTasks(self,logfolder,files):
        for log in os.listdir(logfolder):
            for file in files:
                with open("%s/%s"%(logfolder,log),"r") as f:
                    if file in f.read():
                        return "%s/%s"%(logfolder,log)


def GetLogfile(condor_q):
    all = [i for i in condor_q.split(" ") if len(i.replace(" ",""))]
    return all[9],all[0]

Logger_ = Logger()

print Logger_.Failedjobs_according_Output("tasks/WJetsToQQ_HT-800toInf_APV/log/11081141.log", ["RunIISummer20UL16MiniAODAPVv2WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8106X_mcRun2_asymptotic_preVFP_v11-v22500004DB9CBB8-A4E8-9340-A09B-3AABD34947E0.root",])
print Logger_.LoopTasks("tasks/WJetsToQQ_HT-800toInf_APV/log/std_logs", ["RunIISummer20UL16MiniAODAPVv2WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8106X_mcRun2_asymptotic_preVFP_v11-v22500004DB9CBB8-A4E8-9340-A09B-3AABD34947E0.root",])