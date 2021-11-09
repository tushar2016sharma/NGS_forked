
from pysamimport import pysam
import re, os, hashlib

class SplitBAM(object):
    def __init__(self,bamfile,readgroups,batchsize=10,directory='.',index=False):
        self.bamfile = bamfile
        self.bambase,self.bamextn = self.bamfile.rsplit('.',1)
        self.readgroups = readgroups
        self.batchsize = batchsize
        self.directory = directory
        self.index = index

    def normalize_readgroup(self,rg):
        return re.sub(r'[^A-Z0-9.]','_',rg)

    def readgroup_filename(self,rg):
        uniqstr = hashlib.md5(rg.encode('ascii')).hexdigest().lower()[:5]
        return os.path.join(self.directory,self.bambase + '.' + self.normalize_readgroup(rg) + "." + uniqstr + "." + self.bamextn)

    def iterator(self):
        seenrg = set()
        while True:
            outsam = dict()
            more=False
            samfile = pysam.AlignmentFile(self.bamfile, "rb", require_index=False)
            for al in samfile.fetch(until_eof=True):
                rg = self.readgroups.group(al)
                if rg and rg not in seenrg:
                    if rg not in outsam:
                        if len(outsam) >= self.batchsize:
                            more = True
                            continue
                        else:
                            rgfilename = self.readgroup_filename(rg)
                            outsam[rg] = (rgfilename,pysam.AlignmentFile(rgfilename, "wb", template=samfile))
                    outsam[rg][1].write(al)
            for rg in outsam:
                outsam[rg][1].close()
                if self.index:
                    pysam.index(outsam[rg][0])
                yield rg,outsam[rg][0]
            seenrg.update(outsam)
            outsam = dict()
            if not more:
                break
