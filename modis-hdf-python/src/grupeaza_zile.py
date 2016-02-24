#!/usr/bin/env python
import  os
from grig.modis import configm
from grig.modis.configm import ConfigModis

def isaod(filename=None):
    if filename is None:
        return False;
    if filename.startswith("aod"):
        return True;
    return False;

def iscot(filename=None):
    if filename is None:
        return False;
    if filename.startswith("cot"):
        return True;
    return False;

def extractDay(filename):
    if isaod(filename):
        if len(filename) == 61:
            return filename[27:34]
        else:
            return filename[28:35]
    if iscot(filename):
        if len(filename) == 55 :
            return  filename[21:28]
        else:
            return  filename[22:29]
    return ""

def extractHour(filename):
    if isaod(filename):
        if len(filename) == 61 :
            return filename[35:39]
        else :
            return filename[36:40]
    if iscot(filename):
        if len(filename) == 55 :
            return filename[29:33]
        else :
            return filename[30:34]
    return ""

def minuteDiferenta(filename1, filename2):
    hour1 = extractHour(filename1)
    hour2 = extractHour(filename2)
    timedif = int(hour1) - int(hour2)
    return abs(timedif)

def minuteRealeDiferenta(hour1, hour2):
    ora1 = int(hour1[0:2]) * 60 + int(hour1[2:4])
    ora2 = int(hour2[0:2]) * 60 + int(hour2[2:4])
    dih = ora1 - ora2
    difm = abs(dih)
    return difm

def extrageGrupuri(listforday=[]):
    grupuri = {}
    for i in range(len(listforday)):
        print(str(i) + "  v " + listforday[i])
        hour = extractHour(listforday[i])
        grupexistent = grupuri.get(hour)
        if grupexistent == None:
            for key in sorted(grupuri.keys()):
                difh = int(key) - int(hour)
                if abs(difh) < 20:
                    grupexistent = key
            if grupexistent == None:
                grupuri[hour] = 1
        else:
            pass
    fileGrups = {}
    for key in sorted(grupuri.keys()):
        fileGrups[key] = {"aod":[], "cot":[]}
        print(key)
    for una in listforday:
        hour = extractHour(una)
        if fileGrups.get(hour):
            if isaod(una):
                if fileGrups.get(hour).get("aod"):
                    fileGrups.get(hour).get("aod").append(una)
                else:
                    fileGrups.get(hour)["aod"] = [una]
            if iscot(una):
                if fileGrups.get(hour).get("cot"):
                    fileGrups.get(hour).get("cot").append(una)
                else:
                    fileGrups.get(hour)["cot"] = [una]
        else:
            for unak in fileGrups.keys():
                difh = abs(int(hour) - int(unak))
                if difh < 20:
                    if isaod(una):
                        fileGrups.get(unak).get("aod").append(una)
                    if iscot(una):
                        fileGrups.get(unak).get("cot").append(una)
    return fileGrups

def printgrupari(grupare):
    for grup in sorted(grupare.keys()):
        vari = grupare.get(grup)
        print(grup)
        for tip, files in vari.items():
            for unfil in files:
                print("   " + tip + " " + str(unfil))
    return

def printmath(strday, grupare, filetowrite):
    grupant = {}
    grupantkey = None
    for grup in sorted(grupare.keys()):
        if not grupant:
            grupant = grupare.get(grup)
            grupantkey = grup
            continue
        vari = grupare.get(grup)
        # filtrare in cazul in care am aod anterior dar nu am cot in acest pas
        if not vari.get("cot"):
            grupant = grupare.get(grup)
            grupantkey = grup
            continue;
        minutegrup = minuteRealeDiferenta(grupantkey, grup)
        if minutegrup < 20:
            # exclud grupuri cu timp mic
            continue
        print(strday + "|" + grupantkey + "_" + grup + "|" + str(minutegrup) + "|", filetowrite)
        for aodant in grupant.get("aod"):
            print(aodant + " ", filetowrite)
        print("#", filetowrite)
        grupant = grupare.get(grup)
        grupantkey = grup
        for aodant in vari.get("cot"):
            print(aodant + " ", filetowrite)
        print("", filetowrite)
    return

if __name__ == "__main__":
    os.chdir(ConfigModis.proiectdir)
    lista1 = os.listdir(ConfigModis().proiectdir)
    print(lista1)
    if not os.path.exists(ConfigModis().proiectoutput):
        os.mkdir(ConfigModis().proiectoutput)

    print(os.listdir(ConfigModis().cloudbase))

    aodfiecarean = os.listdir(ConfigModis().aodbase)
    print(aodfiecarean)
    evryaodday = {}
    for unan in aodfiecarean:
        aodinan = os.listdir(ConfigModis().aodbase + "/" + unan)
        aodinan.sort()
        for unfile in aodinan :
            unday = extractDay(unfile)
            hour = extractHour(unfile)
            if unday in evryaodday :
                evryaodday[unday].append(unfile)
            else:
                evryaodday[unday] = []
                evryaodday[unday].append(unfile)
    for key, val in evryaodday.items():
        # print(key+" - size ="+str(len(val)))
        break
    evrycotday = {}
    cotyears = os.listdir(ConfigModis().cloudbase)
    cotyears.sort()
    for uncoty in cotyears:
        cotsiny = os.listdir(ConfigModis().cloudbase + "/" + uncoty)
        cotsiny.sort();
        for unfile in cotsiny:
            unday = extractDay(unfile)
            hour = extractHour(unfile)
            if unday in evrycotday :
                evrycotday[unday].append(unfile)
            else:
                evrycotday[unday] = []
                evrycotday[unday].append(unfile)
        #    print("Fisier "+unfile+"  lungime:"+str(len(unfile))+" unday "+unday+" Am nevoie de ora  gasit:"+hour);
            if unday in evryaodday :
                evryaodday[unday].append(unfile)
            else:
                evryaodday[unday] = []
                evryaodday[unday].append(unfile)
    outfile = open(ConfigModis().gruparezilefile, "w")
    for key in sorted(evryaodday.keys()):
        lungzi = len(evryaodday.get(key))
        print("An zi " + key + " - size =" + str(lungzi))
        # trebuie sa vad cum sunt impartite fisierele, si sfor grup in sorted(grupare.keys()):
        if lungzi < 2 :
            continue
        print("Pentru ziua " + key + " am " + str(lungzi) + " valori")
        valori = evryaodday.get(key)
        grupare = extrageGrupuri(valori)
        # trebuie filtrat outputul sa ramada doar fisierele utilizate
        printgrupari(grupare)
        if len(grupare.keys()) < 2:
            # daca am mai putin de doua grupari nu intereseaza
            continue
        amgrupuri = False
        for tests in valori:
            for testf in valori:
                if isaod(tests) and iscot(testf):
                    if minuteDiferenta(tests, testf) > 20:
                        amgrupuri = True
        if not amgrupuri:
            continue
        aodfirst = False
        amcot = False
        nrgrup = 1
        gruplen = len(grupare.keys())
        for grup in sorted(grupare.keys()):
            vari = grupare.get(grup)
            if nrgrup == 1:
                if "cot" in vari:
                    del vari["cot"]
                    print("remove cot")
                    if len(vari.get("aod")) > 0:
                            aodfirst = True
            if nrgrup > 1 :
                if not aodfirst:
                    if "cot" in vari:
                        del vari["cot"]
                else:
                    if len(vari.get("cot")) > 0:
                        aodfirst = False
                        amcot = True
                        pass
                    if len(vari.get("aod")) > 0:
                        aodfirst = True
            if nrgrup == gruplen:
                del vari["aod"]
                # din ultimul grup am sters aod
            if len(vari.keys()) == 0:
                del grupare[grup]
            nrgrup += 1
        print("dupa filtrare")
        printgrupari(grupare)
        printmath(key, grupare, outfile)

