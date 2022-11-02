# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:26:26 2021

@author: Michael Nauge, Université de Poitiers
"""
import sys


import pandas as pd

import requests
import json


import constantes as myConst 
from api_key_nkl import API_KEY_NKL 

def collectionDatasToDf(targetCollection):
    """
    Obtenir toutes les metas des datas d'une collection nakala 
    dont on connait l'identifiant de collection
    

    Parameters
    targetCollection : STR
        un identifier collection nakala.
        ex : '10.34847/nkl.d9b3cp68'

    Returns
    -------
    dfData : DICT
        un dictionnaire contenant les metadatas des datas
        
    dfFile : DICT
        un dictionnaire contenant les metadatas des files des datas

    """   
    
    # exemple d'url de collection à exporter : 
    # https://apitest.nakala.fr/collections/10.34847/nkl.74aa9b31
    
    
    indexPage = 1
    
    lastPage = sys.maxsize

    # creation de la dataframe Datas avec juste les noms de colonnes pour les datas
    dfData = pd.DataFrame(columns=['linkedInCollection','dataIdentifier','uriData','nkl_title','nkl_created','nkl_license','nkl_type', 'nkl_type_converted','creator_givenname', 'creator_surname', 'creator_orcid'])
    
    # creation de la dataframe Files avec juste les noms de colonnes pour les files
    dfFile = pd.DataFrame(columns=['linkedInData','linkedInData_Title','uriData','name','uriFileDL','description','size','extension','sha1','mime_type','embargoed','uriFileEmbed'])
    
    print("start datas collection extraction")

    while indexPage <= lastPage:
        
    
        url = myConst.API_URL+"/collections/"+targetCollection+"/datas?page="+str(indexPage)+"&limit=10"
        APIheaders = {"X-API-KEY": API_KEY_NKL} 
        
        try : 
            
            response = requests.get(url, headers=APIheaders)
            if response.status_code == 200:
                
                dicoR = json.loads(response.text)
                
                lastPage = dicoR['lastPage']
            
                print(dicoR['currentPage'], " / ", dicoR['lastPage'])
                indexPage +=1
                
                for data in dicoR['data']:
                    dataUri = data["uri"]
                    dataUri = dataUri.replace('https://doi.org/','')
                    
                    print(dataUri,' ', data["status"])
                    
                    dataTitle = ""
                    
                    dicRowData = {}
                    dicRowData['dataIdentifier'] = dataUri
                    dicRowData['uriData'] = myConst.BASE_URL+"/"+dataUri
                    #dicRowData['linkedInCollection'] = data['collectionsIds']
                    
                    for meta in data['metas']:
                        #print(meta['value'], " ", meta['propertyUri'])
                        if meta['propertyUri'] == 'http://nakala.fr/terms#title':
                            #print("title :", meta['value'])
                            dataTitle = meta['value']
                            dicRowData['nkl_title'] = dataTitle
                          
                        if meta['propertyUri'] == 'http://nakala.fr/terms#created':
                            dicRowData['nkl_created'] = meta['value']
                            
                        if meta['propertyUri'] == 'http://nakala.fr/terms#license':
                            dicRowData['nkl_license'] = meta['value']
                          
                        if meta['propertyUri'] == "http://nakala.fr/terms#type":
                            #print("type :",myConst.VOCABTYPE_reverse[meta['value']])
                            dicRowData['nkl_type'] = meta['value']
                            dicRowData['nkl_type_converted'] = myConst.VOCABTYPE_reverse[meta['value']]                       
                            
                    dfData = dfData.append(dicRowData, ignore_index=True) 
                    
                    for file in data['files']:
                        #print(file['name'], file['extension'],file['size'],file['mime_type'],file['sha1'],file['embargoed'],file['description'])
                        #print(">> uriFile", myConst.API_URL+"/data/"+dataUri+"/"+file['sha1'])
                        dicRowFile = file.copy()
                        #dicRowFile = {}
                        dicRowFile['linkedInData'] = dataUri
                        dicRowFile['linkedInData_Title'] = dataTitle
                        dicRowFile['uriData'] = myConst.BASE_URL+"/"+dataUri
                        dicRowFile['uriFileDL'] = myConst.API_URL+"/data/"+dataUri+"/"+file['sha1']
                        dicRowFile['uriFileEmbed'] = myConst.API_URL+"/embed/"+dataUri+"/"+file['sha1']
                        
                        dfFile = dfFile.append(dicRowFile, ignore_index=True)
                        
            else:
                lastPage = indexPage
                print(str(response))
                
        except :
            e = sys.exc_info()[0]
            print("error ", e)
            lastPage = indexPage
    
    return dfData, dfFile
    

def getImageSize(dataIdentifier, fileIdentifier):
    width = 0
    height = 0
        
    url = myConst.API_URL+"/iiif/"+dataIdentifier+"/"+fileIdentifier+"/info.json"
    
    APIheaders = {"X-API-KEY": API_KEY_NKL} 

    
    try :
        response = requests.get(url, headers=APIheaders)
        
        if response.status_code == 200:
            #print(response.text)
            dicoR = json.loads(response.text)
            #print(dicoR)
            width = dicoR['width']
            height = dicoR['height']
    except :
        e = sys.exc_info()[0]
        print("error ", e)

    
    return width, height
    
    
    
def getImageUrlIIIF(dataIdentifier, fileIdentifier, region, size, rotation, quality, formatExt):
    
    
    urlImg = myConst.API_URL+"/iiif/"+dataIdentifier+"/"+fileIdentifier

    urlImg += "/"+region+"/"+size+"/"+rotation+"/"+quality+"."+formatExt

    return urlImg

        

def getSoundTimeDuration(dataIdentifier, fileIdentifier):
    
    # vivement un IIIF A/V !
    
    # je tente une estimation par la taille du fichier, un bitrate standard et on dit qu'on est en mono ?!
    
    
    duration = 0
    

    return duration
    