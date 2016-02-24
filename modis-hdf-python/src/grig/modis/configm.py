'''
Created on Feb 14, 2016

@author: grig
'''
import os

class ConfigModis:
    '''
    classdocs
    '''
    proiectdir = "/com/users/grig/satelit/data"
    proiectoutput = proiectdir + "/gruparezile"
    gruparezilefile = proiectoutput + "/gruparezile.txt"
    cloudbase = proiectdir + "/S06SHAPE/AppModis06C6S/cot"
    aodbase = proiectdir + "/S04SHAPE/AppModis04C6S/aod550Dar"
    grupareziletemp = proiectoutput + "/tmp"
    gruparezilerezult = proiectoutput + "/rezult"
    gruparezilerezulttif = proiectoutput + "/rezult"
    cottiffolder = proiectdir + "/S06SHAPE/AppModis06C6S_2/cot"
    cwptiffolder = proiectdir + "/S06SHAPE/AppModis06C6S_2/cot"
    aod550Dartiffolder = proiectdir + "/S04SHAPE/AppModis04C6S_2/aod550Dar"
    aod550Darsgrdfolder = proiectdir + "/S04SHAPE/AppModis04C6S_1/aod550Dar"
    cotsgrdfolder = proiectdir + "/S06SHAPE/AppModis06C6S_1/cot"
    grupareziletemptif = proiectoutput + "/tmptif"

    def __init__(self):
        '''
        Constructor
        '''

    def isaod(self, filename=None):
        if filename is None:
            return False;
        if filename.startswith("aod"):
            return True;
        return False;

    def iscot(self, filename=None):
        if filename is None:
            return False;
        if filename.startswith("cot"):
            return True;
        return False;

    def extractDay(self, filename):
        if self.isaod(filename):
            if len(filename) == 61:
                return filename[27:34]
            else:
                return filename[28:35]
        if self.iscot(filename):
            if len(filename) == 55 :
                return  filename[21:28]
            else:
                return  filename[22:29]
        return ""

    def extractAn(self, filename):
        if self.isaod(filename):
            if len(filename) == 61:
                return filename[27:31]
            else:
                return filename[28:32]
        if self.iscot(filename):
            if len(filename) == 55 :
                return  filename[21:25]
            else:
                return  filename[22:26]
        return ""

    def extractRadacina(self, filename):
        return os.path.splitext(os.path.basename(filename))[0]

    def extractHour(self, filename):
        if self.isaod(filename):
            if len(filename) == 61 :
                return filename[35:39]
            else :
                return filename[36:40]
        if self.iscot(filename):
            if len(filename) == 55 :
                return filename[29:33]
            else :
                return filename[30:34]
        return ""

    def minuteDiferenta(self, filename1, filename2):
        hour1 = self.extractHour(filename1)
        hour2 = self.extractHour(filename2)
        timedif = int(hour1) - int(hour2)
        return abs(timedif)

    def minuteRealeDiferenta(self, hour1, hour2):
        ora1 = int(hour1[0:2]) * 60 + int(hour1[2:4])
        ora2 = int(hour2[0:2]) * 60 + int(hour2[2:4])
        dih = ora1 - ora2
        difm = abs(dih)
        return difm
