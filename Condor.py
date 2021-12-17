import os
from samples.samples import samples_
from condor.submit_jdl_writer import jdl_writter

class Condor():
    def __init__(self, ConfigPath, samples_toRun, transfer_input_files, transfer_output_files, outputPath, YEAR, DATA_MC, **kwargs):
        self.samples = samples_(ConfigPath).samples()
        self.samples_toRun = samples_toRun
        if self.samples_toRun:
            self.samples = dict([(i,self.samples[i]) for i in self.samples_toRun])
        self.transfer_input_files  = transfer_input_files
        self.transfer_output_files = transfer_output_files
        self.outputPath = outputPath
        self.YEAR = YEAR
        self.DATA_MC = DATA_MC

        self.TaskFolder = "%s/%s"%(os.getcwd(),kwargs.get("TaskFolder","tasks"))
        self.excutable = kwargs.get("excutable","exe.sh")
        self.log = kwargs.get("log","log")
        self.std_logs = "%s/%s/"%(self.log,kwargs.get("std_logs","std_logs"))
        self.MaxRuntime = kwargs.get("MaxRuntime","40000")

        self.init_templete = kwargs.get("init_templete","condor/templete/templete.jdl")
        self.queue_templte = kwargs.get("queue_templte","condor/templete/queue_templte.jdl")
        self.exePath = kwargs.get("queue_templte","condor/templete/")

    def arguments(self, info):
        replace = {
            "DATASET" : info["ds"],
            "INPUTFILE" : info["INPUTFILE"],
            "YEAR" : info["YEAR"],
            "DATA_MC" : info["DATA_MC"],
        }
        return '"{DATASET} {INPUTFILE} {YEAR} {DATA_MC}"'.format(**replace)

    def remaps(self, info):
        replace = {
            "transfer_output_files" : self.transfer_output_files,
            "outputPath" : self.outputPath,
            "ds" : info["ds"],
            "INPUTFILE" : info["INPUTFILE"],
        }
        return '"{transfer_output_files} = {outputPath}/{ds}/{INPUTFILE}"'.format(**replace)

    def Create_Submit_Scripts(self):
        files=os.listdir(self.TaskFolder)
        outputfiles = self.TaskFolder.split("/")[-1]+".sh"
        with open(outputfiles,"w") as f:
            for i in files:
                i = i.replace(" ","").replace("\n","")
                f.write("condor_submit %s/%s/submit.cmd \n"%(self.TaskFolder,i))

    def Generate_Scripts(self):
        for ds in self.samples:
            print "start", ds
            self.jdl_writter = jdl_writter( self.TaskFolder, ds, self.init_templete, self.queue_templte)
            replace = {
                "TaskFolder" : self.TaskFolder,
                "DatasetFolder" : ds,
                "excutable" : self.excutable,
                "transfer_input_files" : self.transfer_input_files,
                "transfer_output_files" : self.transfer_output_files,
                "log" : "%s/%s/%s/"%(self.TaskFolder,ds,self.log),
                "std_logs" : os.path.dirname("%s/%s/%s/"%(self.TaskFolder,ds,self.std_logs)),
                "MaxRuntime" : self.MaxRuntime,
            }
            self.jdl_writter.init(replace, self.log, self.std_logs, self.exePath, self.excutable, self.outputPath, )
            for ifile in self.samples[ds]["files"]:
                info = {
                    "ds" : ds,
                    "INPUTFILE" : ifile,
                    "YEAR" : self.YEAR,
                    "DATA_MC" : self.DATA_MC,
                }
                replace = {
                    "arguments" : self.arguments(info),
                    "transfer_output_remaps" : self.remaps(info),
                }
                self.jdl_writter.add_queue(replace)
        self.Create_Submit_Scripts()

   

# samples_toRun = ["WWW"]
samples_toRun = None

# grid password
grid_password = "365365"
condorpath = os.path.dirname(os.path.realpath(__file__))
os.system("echo "+grid_password+" | voms-proxy-init -voms cms -valid 192:00;cp /tmp/x509up_u{0} ".format(os.getuid())+condorpath) 

Condor_ = Condor(
    "/stash/user/qilongguo/work/gKK/VVVnano/condor/V1/samples/Cust_Nano2016_v9", # ConfigPath
    samples_toRun,
    "%s/%s"%(os.getcwd(),"x509up_u100637"), # transfer_input_files
    "tree.root", # transfer_output_files
    "/stash/user/qilongguo/public/gKK/Ntuple/2016/V1/" , # outputPath
    "2016pre", # YEAR
    "m", # DATA_MC
)
Condor_.Generate_Scripts()
