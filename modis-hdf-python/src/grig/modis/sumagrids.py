'''
Created on Feb 16, 2016

@author: grig
Trebuie sa insumez toate gridurile facute in pasul anterior
'''
from grig.modis.configm import ConfigModis
import os, glob
from string import join
from subprocess import call

def gridsum(inputgr, sumgr):
    call(["saga_cmd", "statistics_grid", "4", "-GRIDS", "\"" + inputgr + "\"", "-SUM", sumgr])
    pass

def gridmaketiff(ingrid, outputtif):
    call(["saga_cmd", "-f=s", "io_gdal", "2", "-OPTIONS", "COMPRESS=DEFLATE", "-FILE",
          outputtif, "-GRIDS", ingrid])
    pass

if __name__ == '__main__':
    os.chdir(ConfigModis.proiectdir)
    lista1 = os.listdir(ConfigModis().gruparezilerezult)

    # print(lista1)
    outputsumarfolder = ConfigModis().proiectoutput + "/sumar"
    if not os.path.exists(outputsumarfolder):
        os.mkdir(outputsumarfolder)

    # for anul in range(2003, 2015):
    grupCalculat = "2003-2015"
    grid = glob.glob(outputsumarfolder + "/year-sum-*.sgrd")
    allgridv = []
    for unfile in grid:
        print(unfile)
        allgridv.append(unfile)
    print("file nr " + str(len(allgridv)))
    allgridstr = join(allgridv, ";")
    sgrdout = outputsumarfolder + "/year-sum-" + grupCalculat + ".sgrd"
    tiffout = outputsumarfolder + "/year-sum-" + grupCalculat + ".tif"
    gridsum(allgridstr, sgrdout)
    gridmaketiff(sgrdout, tiffout)
    # pass

