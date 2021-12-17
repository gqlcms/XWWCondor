import os

class jdl_writter:
    def __init__(self, path, ds, init_templete, queue_templte, filename = "submit.cmd"):
        self.path = "%s/%s/"%(path,ds)
        self.ds = ds
        self.init_templete = init_templete
        self.queue_templte = queue_templte
        self.filename = filename

    # this jdl_writter also 
    # create folder and copy corresponding executable
    # create outfolder
    def init(self,replace, log, std_logs, exePath, excutable, outputPath):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if not os.path.isdir("%s/%s"%(self.path, log)):
            os.makedirs("%s/%s"%(self.path, log))
        if not os.path.isdir("%s/%s"%(self.path, std_logs)):
            os.makedirs("%s/%s"%(self.path, std_logs))
        if not os.path.isdir("%s/%s"%(outputPath, replace["DatasetFolder"])):
            os.makedirs("%s/%s"%(outputPath, replace["DatasetFolder"]))


        os.system("cp %s/%s %s"%( exePath, excutable, self.path))

        with open(self.init_templete,"r") as fin:
            with open(self.path+self.filename,"w") as fout:
                fout.write(fin.read().format(**replace))

    def add_queue(self,replace,):
        with open(self.queue_templte,"r") as fin:
            with open(self.path+self.filename,"a+") as fout:
                fout.write(fin.read().format(**replace))

    