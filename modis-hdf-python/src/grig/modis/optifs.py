'''
Created on Feb 14, 2016
@author: grig
'''
from grig.modis.configm import ConfigModis
from re import split
from subprocess import call
import osgeo.gdal

def printTiffileGeoinfo(sgrdfile):
    dataset = osgeo.gdal.Open(sgrdfile)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize  # print(" cols " + str(cols))
    geotransform = dataset.GetGeoTransform()
    print("%s cols %d, rows %d, %s " % (sgrdfile, cols, rows, str(geotransform)))



def gridmosaickos(ingrids, outputgrid):
    call(["saga_cmd", "-f=s", "grid_tools", "3", "-INTERPOL=0", "-OVERLAP=4", "-TARGET_OUT_GRID=" + outputgrid,
          "-TARGET_DEFINITION=0", "-TARGET_USER_XMIN=19.80000 ", "-TARGET_USER_XMAX=30.05000", "-TARGET_USER_YMIN=43.22000", "-TARGET_USER_YMAX=48.5400",
          "-TARGET_USER_SIZE=0.0510", "-GRIDS", ingrids])
    pass

def gridmaketiff(ingrid, outputtif):
    call(["saga_cmd", "-f=s", "io_gdal", "2", "-OPTIONS", "COMPRESS=DEFLATE", "-FILE",
          outputtif, "-GRIDS", ingrid])
    pass

def gridreclassaod(ingrid, reclassgrid):
    call(["saga_cmd", "-f=s", "grid_tools", "15", "-INPUT", ingrid, "-RESULT", reclassgrid, "-METHOD=1", "-MIN=-0.1", "-MAX=10", "-RNEW=1", "-ROPERATOR=1"])
    pass

def gridreclasscot(ingrid, reclassgrid):
    call(["saga_cmd", "-f=s", "grid_tools", "15", "-INPUT", ingrid, "-RESULT", reclassgrid, "-METHOD=1", "-MIN=-0.1", "-MAX=200", "-RNEW=1"])
    pass

def gridsum(inputgr, sumgr):
    call(["saga_cmd", "-f=s", "grid_calculus", "8", "-GRIDS", inputgr, "-RESULT", sumgr])
    pass

if __name__ == '__main__':
    print("Rulez main in modul, grupfile:" + ConfigModis.gruparezilefile)
    fisiergrupuri = open(ConfigModis.gruparezilefile, mode='r')
    for grupinline in fisiergrupuri:
        params = split("\|", grupinline)
        # print(str(params))
        dayofgrup = params[0];
        grupname = params[1]
        minute = params[2]
        fisierecamp = params[3]
        fg = split("#", fisierecamp)
        fisiereaod = split(" ", str.strip(fg[0], ' \n\r'))
        fisierecot = split(" ", str.strip(fg[1], ' \n\r'))
        conm = ConfigModis()
        sumaodgrid = ""
        if len(fisiereaod) == 1:
            fileaod = fisiereaod[0]
            an = conm.extractAn(fileaod)
            radacina = conm.extractRadacina(fileaod)
            sgrdfile = ConfigModis.aod550Darsgrdfolder + "/" + an + "/" + radacina + ".sgrd"
            sumaodgrid = sgrdfile
        else:
            fisieresgrdf = []
            radacina = ""
            for fileaod in fisiereaod:
                an = conm.extractAn(fileaod)
                radacina = conm.extractRadacina(fileaod)
                sgrdf = ConfigModis.aod550Darsgrdfolder + "/" + an + "/" + radacina + ".sgrd"
                fisieresgrdf.append(sgrdf)
            paramsfile = ";".join(fisieresgrdf)
            # print(paramsfile)
            outputgrid = ConfigModis.grupareziletemp + "/" + radacina + ".sgrd"
            gridmosaickos(paramsfile, outputgrid)
            sumaodgrid = outputgrid
        print("Fisier AOD " + sumaodgrid)
        gridptcot = ""
        if len(fisierecot) == 1:
            fileaod = fisierecot[0]
            an = conm.extractAn(fileaod)
            radacina = conm.extractRadacina(fileaod)
            sgrdfile = ConfigModis.cotsgrdfolder + "/" + an + "/" + radacina + ".sgrd"
            gridptcot = sgrdfile
        else:
            fisieresgrdf = []
            radacina = ""
            for fileaod in fisierecot:
                an = conm.extractAn(fileaod)
                radacina = conm.extractRadacina(fileaod)
                sgrdf = ConfigModis.cotsgrdfolder + "/" + an + "/" + radacina + ".sgrd"
                fisieresgrdf.append(sgrdf)
            paramsfile = ";".join(fisieresgrdf)
            # print(paramsfile)
            outputgrid = ConfigModis.grupareziletemp + "/" + radacina + ".sgrd"
            gridmosaickos(paramsfile, outputgrid)
            gridptcot = outputgrid
        print("Fisier COT " + gridptcot)
        reclassaod = ConfigModis.grupareziletemp + "/" + conm.extractRadacina(sumaodgrid) + "-recl.sgrd";
        reclasscot = ConfigModis.grupareziletemp + "/" + conm.extractRadacina(gridptcot) + "-recl.sgrd";
        gridreclassaod(sumaodgrid, reclassaod)
        gridreclasscot(gridptcot, reclasscot)
        print("Fisier AOD reclass" + reclassaod)
        print("Fisier COT reclass" + reclasscot)
        # tifaod = ConfigModis.grupareziletemptif + "/" + conm.extractRadacina(reclassaod) + ".tif";
        # tifcot = ConfigModis.grupareziletemptif + "/" + conm.extractRadacina(reclasscot) + ".tif";
        # gridmaketiff(reclassaod, tifaod)
        # gridmaketiff(reclasscot, tifcot)

        fiserfinalsgrd = ConfigModis.gruparezilerezult + "/" + dayofgrup + "-" + grupname + ".sgrd"
        fiserfinaltif = ConfigModis.gruparezilerezulttif + "/" + dayofgrup + "-" + grupname + ".tif"
        # gridmaketiff(fiserfinalsgrd, fiserfinaltif)
        gridsum(reclassaod + ";" + reclasscot, fiserfinalsgrd)
        gridmaketiff(fiserfinalsgrd, fiserfinaltif)
        print("Fisier final :" + fiserfinaltif)


'''Mosaicking
Parameters
Input Grids: 2 objects (aod550Dar_2005_10_MOD04_L2.A2005286.0850.006.2014348072330, aod550Dar_2005_10_MOD04_L2.A2005286.0855.006.2014348072407)
Preferred data storage type: 4 byte floating point
Interpolation: Nearest Neighbor
Overlapping Areas: mean
Blending Distance: 10.000000
Match: regression
Target Grid System: user defined
Left: 19.800000
Right: 30.051000
Bottom: 43.220000
Top: 48.524000
Cellsize: 0.051000
Fit: nodes
Grid System: <not set>
Target Grid: <create>
'''


