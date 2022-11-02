# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:48:05 2021

@author: Michael Nauge, Université de Poitiers
"""


import sys

import nklPushCorpus as npc


def post_datas_uploads_test():
    
    pathFiles = "./../data/phw-1972-112-7.jpg"
    
    print("try to send"+pathFiles)

    try :
        shaRes = npc.post_datas_uploads(pathFiles)
        
        print(shaRes)
        
    except ValueError:
        print("Upload file error")
    
def post_datas_addFile_test(dataIdentifier):
    
     pathFile = "./../data/phw-1972-112-126.jpg"
     
     descriptionFile = "un file ajouté après"
     
     npc.post_datas_addFile(dataIdentifier, pathFile, descriptionFile)
     
    
def post_datas_test(collectionId):
    
    listFilesDescriptions = []
    listFilesDescriptions.append({"pathFile":"./../data/phw-1972-112-7.jpg", "descriptionFile":"huuhu mon beau file 7"})
    listFilesDescriptions.append({"pathFile":"./../data/phw-1972-112-8.jpg", "descriptionFile":"yes mon beau file 8"})

    
    #listFiles = ["./../data/phw-1972-112-8.jpg", "./../data/phw-1972-112-7.jpg"]

    dicoMetas = {}
    dicoMetas["collectionsIds"] = [collectionId]

    #dicoMetas["status"] = "pending"
    dicoMetas["status"] = "published"

    dicoMetas["metas"] = []
    
    metaType = {"value": "http://purl.org/coar/resource_type/c_c513",
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
                "propertyUri": "http://nakala.fr/terms#type"
                }
    dicoMetas["metas"].append(metaType)
    
    
    metaTitle={"value": "DBG - Charles Aubrière jouant du violon",
      "lang": "fr",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string",
      "propertyUri": "http://nakala.fr/terms#title"
      }
    dicoMetas["metas"].append(metaTitle)

    metaAuthor = {"value": {
        "givenname": "Mic",
        "surname": "Mac",
        "orcid":"0000-0000-4242-4242"
         },
      "propertyUri": "http://nakala.fr/terms#creator"
      }
    dicoMetas["metas"].append(metaAuthor)
    
    metaCreated={"value": "1961-01-01",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string",
      "propertyUri": "http://nakala.fr/terms#created"
    }
    dicoMetas["metas"].append(metaCreated)
    
    metaLicense={"value": "CC-BY-4.0",
                 "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                 "propertyUri": "http://nakala.fr/terms#license"
                 }
    dicoMetas["metas"].append(metaLicense)
   

    handle = npc.post_datas(dicoMetas, listFilesDescriptions)
    
    print("data handle:",handle)

    return handle

   
def put_datas_test(dataIdentifier):
    #changement de date    
    dicoMetas = {}
    
    dicoMetas["metas"] = []
    
    metaType = {"value": "http://purl.org/coar/resource_type/c_c513",
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
                "propertyUri": "http://nakala.fr/terms#type"
                }
    dicoMetas["metas"].append(metaType)
        
    metaTitle={"value": "DBG - Charles Aubrière jouant du violon",
      "lang": "fr",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string",
      "propertyUri": "http://nakala.fr/terms#title"
      }
    dicoMetas["metas"].append(metaTitle)

    metaAuthor = {"value": {
        "givenname": "Mic",
        "surname": "Mac",
        "orcid":"0000-0000-4242-4242"
         },
      "propertyUri": "http://nakala.fr/terms#creator"
      }
    dicoMetas["metas"].append(metaAuthor)
    
    metaCreated={"value": "1969-09-07",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string",
      "propertyUri": "http://nakala.fr/terms#created"
    }
    dicoMetas["metas"].append(metaCreated)
    
    metaLicense={"value": "CC-BY-4.0",
                 "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                 "propertyUri": "http://nakala.fr/terms#license"
                 }
    dicoMetas["metas"].append(metaLicense)
    
    npc.put_datas(dataIdentifier, dicoMetas,[])

def delete_datas_test(dataIdentifier):
    npc.delete_datas(dataIdentifier)

def delete_datasByTitle_test():
    dataTile = "DBG - Charles Aubrière jouant du violon"
    npc.delete_datasByTitle(dataTile)
    
    
def get_data_byId_test():
    
    idData = "10.34847/nkl.a8301jsb"
    dicMetas = npc.get_data_byId(idData)
    print(dicMetas)
    
    
    
def get_dataIdentifier_byNklTitle_test():
    title = "DBG - Charles Aubrière jouant du violon"
    dataIdentifier = npc.get_dataIdentifier_byNklTitle(title)
    
    print(dataIdentifier)
 
def get_fileExistInData_test():
    dataIdentifier = "10.34847/nkl.7e00q4yf"
    filename = "phw-1972-112-7.jpg"
    fileExist = npc.get_fileExistInData(dataIdentifier, filename)
    print(fileExist)
    
    dataIdentifier = "10.34847/nkl.7e00q4yf"
    filename = "phw-1972-112-8.jpg"
    fileExist = npc.get_fileExistInData(dataIdentifier, filename)
    print(fileExist)
    
    
def update_status():
        
    dataIdentifier = "10.34847/nkl.2fddom1e"
    
    dicoMetas = {}
    
    dicoMetas["status"] = "pending"

    
    npc.put_datas(dataIdentifier, dicoMetas,[])
    
    '''
    <Response [422]>
    {"code":422,"message":"Published data : status can't be changed","payload":[]}
    put data error"
    '''
    
    
def post_collections_test():
    
    # création du dictionnaire qui sera converti en json
    dicoMetas = {}
    
    # choisir la valeur du status de la collection
    # soit public soit private
    dicoMetas["status"] = "public"
    
    dicoMetas["metas"] = []
    # création de la méta nakala_title
    # c'est la seule méta obligatoire
    metaTitle={"value": "DBG - Collection data multifile avec descriptions",
      "lang": "fr",
      "typeUri": "http://www.w3.org/2001/XMLSchema#string",
      "propertyUri": "http://nakala.fr/terms#title"
      }
    dicoMetas["metas"].append(metaTitle)
    
    # appel de la fonction de création de collection
    # avec les métadonnées déclarée ci-dessus
    handle = npc.post_collections(dicoMetas)
    # si tout se passe bien la fonction nous retourne
    # la handle de la collection créée sur nakala
    print("collection handle:", handle)
    return handle
    
    
def post_datas_addUserRights_test():
    
    handleData = "10.34847/nkl.786e4wz4"
    
    idUserGroup = "64500ddf-cdd8-11eb-817d-5254008c9c26"
    
    rights = "ROLE_ADMIN"
    
    npc.post_datas_addUserRights(handleData, idUserGroup, rights)
    
    #print("url pour vérification visuelle : ")
    #print("https://apitest.nakala.fr/datas/"+handleData+"/rights")

    
def post_collections_addUserRights_test():
    
    handleCollection = "10.34847/nkl.9401020v"
    
    idUserGroup = "64500ddf-cdd8-11eb-817d-5254008c9c26"
    
    rights = "ROLE_ADMIN"
    
    npc.post_collections_addUserRights(handleCollection, idUserGroup, rights)
    
    print("url pour vérification visuelle : ")
    print("https://apitest.nakala.fr/collections/"+handleCollection+"/rights")
    


def main(argv):
    #handleCollection = post_collections_test()
    #print("le lien pour consulter la collection: "+"https://test.nakala.fr/collection/"+handleCollection)
   
    #post_datas_uploads_test()
    
    #handleData = post_datas_test(handleCollection)
    #print("le lien pour consulter la data: "+"https://test.nakala.fr/"+handleData)
    
    
    #post_datas_addFile_test(handleData)
    
    
    #put_datas_test(handleData)
    
    #get_data_byId_test()
    #get_dataIdentifier_byNklTitle_test()
    #get_fileExistInData_test()
    
    #delete_datasByTitle_test()

    #update_status()
    
    #delete_datas_test(handleData)
    
    #post_datas_addUserRights_test()
    post_collections_addUserRights_test()
    
    
    pass
    
    
if __name__ == "__main__":
    main(sys.argv) 