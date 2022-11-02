# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:02:26 2021

@author: Michael Nauge, Université de Poitiers
"""
import sys

import nklPullCorpus as npcPull


import pandas as pd

from skimage import io
 

def collectionToDf_test():
    #targetCollection = "10.34847/nkl.188ei077"
    #targetCollection = "10.34847/nkl.d9b3cp68"
    
    
    
    
    targetCollection = "10.34847/nkl.ffabdg38"
    
    
    dfData, DfFile = npcPull.collectionDatasToDf(targetCollection)
    
    #DfFile.to_excel("./../data/outputDbgFiles.xlsx", index = False)
    
    
    
    writer = pd.ExcelWriter('./../data/outputDbgFiles.xlsx') 
    DfFile.to_excel(writer, sheet_name='files_sheet', index=False, na_rep='NaN')
    dfData.to_excel(writer, sheet_name='datas_sheet', index=False, na_rep='NaN')

    # Auto-adjust columns' width
    widthMax=80
    for column in DfFile:
        column_width = max(DfFile[column].astype(str).map(len).max(), len(column))
        column_width = min(column_width, widthMax)
                
        col_idx = DfFile.columns.get_loc(column)
        writer.sheets['files_sheet'].set_column(col_idx, col_idx, column_width)
        
    for column in dfData:
       column_width = max(dfData[column].astype(str).map(len).max(), len(column))
       column_width = min(column_width, widthMax)
               
       col_idx = dfData.columns.get_loc(column)
       writer.sheets['datas_sheet'].set_column(col_idx, col_idx, column_width)
       
    writer.save()
    
    
def getImageSize_test():
    dataIdentifier = "10.34847/nkl.f1ea3017"
    fileIdentifier = "ebe638b652e63a8ac88dcd3f5badcecab3f3119b"
    
    w,h = npcPull.getImageSize(dataIdentifier, fileIdentifier)
    print(w,h)
        
def getImageByIIIF_test():
    dataIdentifier = "10.34847/nkl.f1ea3017"
    fileIdentifier = "ebe638b652e63a8ac88dcd3f5badcecab3f3119b"


    #"3976,3143,870,618" permet une extraction à partir de l'image d'origine 
    #d'un rectangle commençant au pixel 3976 sur l'axe horizontal, 
    #3143 sur l'axe vertical, et de dimension de 870 pixels de largeur et 
    #618 pixels de hauteur
    
    region = "0,0,400,400"

    #full ou par exemple 800, 600
    #est la taille de l'image cible générée en pixels. 
    #Si on choisit la valeur full, l'image extraite est 
    #fournie à la meilleure taille disponible 
    size = 'full'

    #correspond à un angle de rotation pour l'image cible 
    #(en degrés, dans le sens des aiguilles d'une montre; par exemple "90") 
    rotation  = "0"
    
    #default, gray, bitonal 
    quality = 'default'
    
    #'png, jpg, jp2, pdf, gif, tif'
    formatExt  = 'jpg'
    
    urlImg = npcPull.getImageUrlIIIF(dataIdentifier, fileIdentifier, region, size, rotation, quality, formatExt)
    print(urlImg)

    img = io.imread(urlImg)
    pathImgFileOut = "./../data/dbgImg.jpg"
    io.imsave(pathImgFileOut, img)
    
    
def getSoundTimeDuration_test():

    
    dataIdentifier = "10.34847/nkl.7f44gtj0"
    fileIdentifier = "206f92670979917a79a208788e65c2fa4c48634c"
    
    d = npcPull.getSoundTimeDuration(dataIdentifier, fileIdentifier)
    print(d)
    
    
    
def main(argv):
    #collectionToDf_test()
    #getImageSize_test()
    getImageByIIIF_test()
    #getSoundTimeDuration_test()
    
if __name__ == "__main__":
    main(sys.argv) 