import os
class samples:
    def __init__(self, ConfigPath):
        self.ConfigPath = ConfigPath
        self.Samples = {}
        for i in os.listdir(ConfigPath):
            self.Samples[i.replace(".txt","")] = {}
            self.Samples[i.replace(".txt","")]["filelist"] = "%s/%s"%(ConfigPath,i)

    def samples(self):
        for i in self.Samples:
            self.Samples[i]["files"] = []
            with open(self.Samples[i]["filelist"],"r") as f:
                for ifilein in f.readlines():
                    self.Samples[i]["files"].append(ifilein.replace("\n","").replace(" ",""))
        return self.Samples

samples_ = lambda ConfigPath: samples(ConfigPath)
