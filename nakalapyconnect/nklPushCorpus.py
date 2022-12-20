# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:42:17 2021

@author: Michael Nauge (Université de Poitiers)
"""

import requests
import json

import constantes as myConst
from api_key_nkl import API_KEY_NKL


class NakalaException(Exception):
    pass

#-----------------------------------------------------------------------------
# COLLECTION
#-----------------------------------------------------------------------------
def get_collection_byId(collectionId):
    """
    Obtenir toutes les metas d'une collection nakala dont on connait le doi


    Parameters
    dataId
    dataTitle : STR
        un identifier nakala.

    Returns
    -------
    dicoMetas :DICT
        un dictionnaire contenant les metadatas obtenus depuis la reponse json du server


    """

    # https://apitest.nakala.fr/collections/10.34847/nkl.74aa9b31

    url = myConst.API_URL+"/collections/"+collectionId
    APIheaders = {"X-API-KEY": API_KEY_NKL}

    try :

        response = requests.get(url, headers=APIheaders)
        if response.status_code == 200 :

            dicoMetas = json.loads(response.text)

            return dicoMetas
        else:
            print(str(response))
            raise NakalaException(response.text)

    except NakalaException:
        print("error request")





def post_collections(dicoMetas):
    """
    Fonction permettant la création d'un collection Nakala.
    Il est probablement judicieux de vérifier en amont l'existance
    éventuelle de cette collection pour ne pas la re-créer si elle existe déjà.
    Par exemple avec une requete du genre getCollectionIdentifierByTitle.

    Parameters
    ----------
    dicoMetas : DICT
        un dictionaire python (qui sera converti en json) contenant les
        métadonnées de la collection.
        Plus d'informations sur les métadonnées à renseigner :
        https://apitest.nakala.fr/doc#operations-collections-post_collections

    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    Le handle de la collection si la création c'est bien passé.

    """
    url = myConst.API_URL+"/collections"
    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url, data =json.dumps(dicoMetas), headers=APIheaders)

    """
    # traiter la réponse du server
    # réponse 201 c'est que la création c'est bien passée.
    # sinon c'est qu'il y a eu un soucis.
    if not response.status_code == 201 :
        print(str(response))
        print(str(response.text))
        raise NakalaException(response.text)
    else:
    # tout c'est bien passé donc on a un
    # identifier/handle à récupérer dans le json retourné par le server
       print(response.text)

       json_resp = json.loads(response.text)
       handle = json_resp['payload']['id']

       return handle
       """

    return response

#-----------------------------------------------------------------------------
# DATA
#-----------------------------------------------------------------------------

def get_data_byId(dataId):
    """
    Obtenir toutes les metas d'une data nakala dont on connait le doi


    Parameters
    dataId
    dataTitle : STR
        un identifier nakala.

    Returns
    -------
    dicoMetas :DICT
        un dictionnaire contenant les metadatas obtenus depuis la reponse json du server


    """

    # https://apitest.nakala.fr/datas/10.34847/nkl.a8301jsa

    url = myConst.API_URL+"/datas/"+dataId
    APIheaders = {"X-API-KEY": API_KEY_NKL}


    try :

        response = requests.get(url, headers=APIheaders)
        if response.status_code == 200:

            dicoMetas = json.loads(response.text)

            return dicoMetas
        else:
            print(str(response))
            raise NakalaException(response.text)

    except NakalaException:
        print("error request")




def get_dataIdentifier_byNklTitle(dataTitle):
    """
    Afin d'éviter d'envoyer plusieurs fois la même donnée,
    il est important de pouvoir vérifier qu'elle n'éxiste pas déjà.
    Cette fonction permet d'obtenir le handle d'une data si elle existe en
    interrogent le champs "nakala title"
    Attention : ceci est une fonction qui doit être améliorée en utilisant les
    fonctionnalitées plus avancées de filtrage lorsque celà sera disponible.
    Il faudrait pouvoir préciser un handle de collection mère de cette data
    par exemple. Afin d'éviter d'identifier une data d'un meme nom créée par quelqu'un d'autre
    En effet, il n'y a pas de filtrage côté nakala qui évite la création de datas de même title.


    Parameters
    ----------
    dataTitle : STR
        le titre de la data (le nakala title).

    Returns
    -------
    dataIdentifier :LIST(STR)
        une liste contenant le handle de la data si il existe une data contenant ce titre exactement,
        sinon le dataIdentifier est une liste vide.


    """

    # le code ci dessous construit un requete de ce genre :
    # https://api.nakala.fr/search?q=DBG - Charles Aubrière jouant du violon&fq=scope=data&order=relevance&page=1&size=25


    url = myConst.API_URL+"/search?q="+dataTitle+"&fq=scope=data&order=relevance&page=1&size=25"
    APIheaders = {"X-API-KEY": API_KEY_NKL}

    #la liste à retourner
    listDataIdentifier = []

    try :

        response = requests.get(url, headers=APIheaders)

        json_resp = json.loads(response.text)

        listData = json_resp['datas']

        for objData in listData:
            for metas in objData['metas']:
                if metas['value'] == dataTitle and metas['propertyUri'] == "http://nakala.fr/terms#title":

                    listDataIdentifier.append(objData['identifier'])

        return listDataIdentifier

    except NakalaException:
        print("error request")
        raise NakalaException(response.text)


def get_fileExistInData(dataIdentifier, filename):
    """
    Cette fonction permet de vérifier l'existance d'un
    fichier (désigné par son nom) dans une
    data (désigné par son handle/dataIdentifier)

    Cette fonction peut être utilisé pour éviter d'ajouter un
    fichier à une data alors qu'elle le contient déjà.

    Parameters
    ----------
    dataIdentifier : STR
        le handle d'une data.
    filename : STR
        le nom du fichier que nous cherchons.

    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    bool
        retourne True si il existe un fichier du même nom
        dans la data identifié par son handle.

    """

    url = myConst.API_URL+"/datas/"+dataIdentifier+"/files"
    APIheaders = {"X-API-KEY":API_KEY_NKL}



    response = requests.get(url, headers=APIheaders)

    if response.status_code == 200 :
        json_resp = json.loads(response.text)

        for file in json_resp:

            if filename==file['name']:
                return True
        return False
    else:
        raise NakalaException(response.text)





def post_datas_uploads(pathFile):
    """
    Avant de pouvoir créer une data nakala contenant un fichier
    il faut avoir préalablement envoyé le fichier.

    Il faut donc utiliser cette fonction pour envoyer un fichier.
    Une fois le fichier reçu sur nakala,
    le serveur nous retourne le SHA-1 du fichier.
    Ce fichier est stocké dans un espace temporaire de traitement.


    Parameters
    ----------
    pathFile : STR
        le chemin local vers le fichier à envoyer.


    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    STR
        Le SHA-1 du fichier à utiliser pour dépôt d'une data.

    """


    url = myConst.API_URL+"/datas/uploads"

    headers = {"X-API-KEY":API_KEY_NKL, "accept": "application/json"}

    fileOpened = open(pathFile, "rb")
    fileCur = {'file': fileOpened}

    response = requests.post(url, files=fileCur, headers=headers)

    if not response.status_code == 201 :
        print(str(response))
        print(str(response.text))
        raise NakalaException(response.text)

    else:

        json_resp = json.loads(response.text)
        return json_resp['sha1']




def post_datas(dicoMetas, listFilesDescriptions):
    """
    Cette fonction permet de déposer une data dans nakala avec son jeu de
    métadonnées descriptives et une liste de fichier.

    TODO :
        - il faudrait améliorer cette fonction pour ajouter
    des métadonnées différentes à chaque file de la data.
        - dans le cas d'une data multi-file, il pourrait être possible de
        lancer les uploads en parallèles dans des threads.


    Parameters
    ----------
    dicoMetas : DICTIONARY
        un dictionaire python (qui sera converti en json) contenant les
        métadonnées.
        Pour plus d'informations sur les valeurs possibles à mettre
        dans le dictionnaire :
            https://apitest.nakala.fr/doc#operations-datas-post_datas


    listFilesDescriptions : LIST
        une liste contenant des dictionnaires contenant
        "pathFile":STR le chemin de fichier à envoyer.
        "descriptionFile":STR la description du fichier

    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    handle

    """


    url = myConst.API_URL+"/datas"
    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}

    # pour chaque file il faut faire une requete post upload séparée
    # et penser à conserver l'identifiant SHA1 du file arrivée sur nakala

    dicoMetas["files"] = []

    for pathFileDesc in listFilesDescriptions:
        #import pdb ; pdb.set_trace()
#        sha1Cur = post_datas_uploads(pathFileDesc)#['pathFile'])
#        dicoMetas["files"].append({'sha1':sha1Cur,'description':pathFileDesc})#['descriptionFile']})

        sha1Cur = post_datas_uploads(pathFileDesc['pathFile'])
        dicoMetas["files"].append({'sha1':sha1Cur,'description':pathFileDesc['descriptionFile']})


    # envoyer la requete post data
    response = requests.post(url, data =json.dumps(dicoMetas), headers=APIheaders)

    # traiter la réponse du server
    # réponse 201 c'est que la création c'est bien passée.
    # sinon c'est qu'il y a eu un soucis.
    if not response.status_code == 201 :
        print("Warning : ",str(response))
        print(str(response.text))
        raise NakalaException(response.text)

    else:
    # tout c'est bien passé donc on a un
    # identifier/handle à récupérer dans le json retourné par le server
       print(response.text)
       json_resp = json.loads(response.text)
       handle = json_resp['payload']['id']

       return handle


def post_datas_addFile(dataIdentifier, pathFile, descriptionFile):
    """
    Fonction permettant d'ajouter un fichier à une data existante

    Parameters
    ----------
    dataIdentifier : STR
        Le handle de la data à compléter.

    pathFile : STR
        Le chemin vers le fichier à envoyer

    descriptionFile : STR
        La description du fichier


    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    None
    """


    url = myConst.API_URL+"/datas/"+dataIdentifier+"/files"
    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}


    dicoMetas = {}

    sha1Cur = post_datas_uploads(pathFile)
    dicoMetas['sha1'] = sha1Cur
    dicoMetas['description']=descriptionFile


     # envoyer la requete pos datas/files
    response = requests.post(url, data =json.dumps(dicoMetas), headers=APIheaders)


    if not response.status_code == 200 :
         print(str(response))
         print(str(response.text))
         raise NakalaException(response.text)

    else:
        json_resp = json.loads(response.text)
        print(json_resp)



def put_datas(dataIdentifier, dicoMetas, pathFiles):
    """
    Fonction permettant de mettre à jour une data nakala (métas et/ou file)
    Plus d'informations sur les métadonnées à renseigner :
        https://apitest.nakala.fr/doc#operations-datas-put_datas__identifier_

    TODO :
        -ajouter la gestion d'ajout de fichiers additionnels car pour le moment
        seulement les métadonnées descriptives sont mis à jour.

    Parameters
    ----------
    dataIdentifier : STR
        Le handle de la data à modifier.
    dicoMetas : DICT
        un dictionaire python (qui sera converti en json) contenant les
        nouvelles métadonnées...
    pathFiles : LIST
        une liste contenant des chemins de fichier à ajouter.

    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    None.

    """
    url = myConst.API_URL+"/datas/"+dataIdentifier
    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}


    # envoyer la requete put datas
    response = requests.put(url, data =json.dumps(dicoMetas), headers=APIheaders)

    # traiter la réponse du server
    # réponse 204 c'est que la MAJ c'est bien passée.
    # sinon c'est qu'il y a eu un soucis.
    if not response.status_code == 204 :
        print("Warning : ",str(response))
        print(str(response))
        print(str(response.text))
        raise NakalaException(response.text)

    else:
    # tout c'est bien passé
        print(str(response))
        print("data updated")


def delete_datas(dataIdentifier):
    """
    fonction permettant de supprimer une data nakala identifié par son
    handle

    Parameters
    ----------
    dataIdentifier : STR
        le handle de la data.

    Raises
    ------
    NakalaException
        Lève des exceptions si le serveur répond par un message d'erreur.

    Returns
    -------
    None.

    """
    url = myConst.API_URL+"/datas/"+dataIdentifier
    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json"}

    response = requests.delete(url, headers=APIheaders)

    # traiter la réponse du server
    # réponse 204 c'est que la MAJ c'est bien passée.
    # sinon c'est qu'il y a eu un soucis.
    if not response.status_code == 204 :
        print(str(response))
        print(str(response.text))
        raise NakalaException(response.text)
    else:
    # tout c'est bien passé
        print(str(response.text))


def delete_datasByTitle(dataTile):
    """
    Fonction permettant de supprimer une data identifié par son nakala title.
    Cette fonction commence par chercher le handle de la data par son title.
    Si il y a un exact matching,
    la fonction appel la fonction delete_datas(dataIdentifier)

    Parameters
    ----------
    dataTile : STR
        le titre d'une data nakala.

    Returns
    -------
    None.

    """
    dataIdentifier = get_dataIdentifier_byNklTitle(dataTile)
    if len(dataIdentifier)>0:
        delete_datas(dataIdentifier)
        print("data deleted")
    else:
        print("data not found")




def post_datas_addUserRights(dataIdentifier, idUserGroup, rights):
    """
    Fonction permettant d'ajouter des droits à un utilisateur ou
    à un group d'utilisateurs sur une data cible.

    Rappel : Il existe deux instances de nakala :
        nakala (production) : https://nakala.fr
        nakala (test) : https://test.nakala.fr
        Il n'est pas possible d'ajouter à une data sur l'instance test
        des groupes utilisateurs de l'instance production


    Parameters
    ----------
    dataIdentifier : STR
        le handle de la data.

    idUserGroup : STR
        l'identifiant de l'utilisateur ou du group utilisateur
        exemple : id user group : f4f565c4-646b-11eb-817d-5254008c9c26

    rights : STR
        le droit attribué à l'utilisateur sur la data cible
        valeurs possibles : "ROLE_ADMIN", "ROLE_EDITOR", "ROLE_READER", "ROLE_OWNER"

    Returns
    -------
    None.
    """


    url = myConst.API_URL+"/datas/"+dataIdentifier+"/rights"
    print(url)

    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json"}

    # attention il faut mettre le dicoRights dans une liste !
    # cf exemple dans la doc
    listRights = []

    dicoRights = {}
    dicoRights['id'] = idUserGroup
    dicoRights['role'] = rights

    listRights.append(dicoRights)


    response = requests.post(url, data =json.dumps(listRights), headers=APIheaders)

    if response.status_code == 200:
        dicoR = json.loads(response.text)

        print(dicoR)
    else:

        print("error")
        print(response.text)


def post_collections_addUserRights(collectionIdentifier, idUserGroup, rights):
    """
    Fonction permettant d'ajouter des droits à un utilisateur ou
    à un group d'utilisateurs sur une collection cible.

    Attention, cela n'affecte que la collection mais pas les datas filles.
    Si besoin, il faut appeler post_datas_addUserRights pour chaque datas
    aggrégées par la collection.

    TODO : créer une fonction qui fait les appels en boucle pour toutes
    les datas d'une collection'



    Parameters
    ----------
    dataIdentifier : STR
        le handle de la collection.

    idUserGroup : STR
        l'identifiant de l'utilisateur ou du group utilisateur
        exemple : id user group : f4f565c4-646b-11eb-817d-5254008c9c26

    rights : STR
        le droit attribué à l'utilisateur sur la data cible
        valeurs possibles : "ROLE_ADMIN", "ROLE_EDITOR", "ROLE_READER", "ROLE_OWNER"

    Returns
    -------
    None.
    """


    url = myConst.API_URL+"/collections/"+collectionIdentifier+"/rights"
    print(url)

    APIheaders = {"X-API-KEY":API_KEY_NKL, "accept": "application/json"}

    # attention il faut mettre le dicoRights dans une liste !
    # cf exemple dans la doc
    listRights = []

    dicoRights = {}
    dicoRights['id'] = idUserGroup
    dicoRights['role'] = rights

    listRights.append(dicoRights)


    response = requests.post(url, data =json.dumps(listRights), headers=APIheaders)

    if response.status_code == 200:
        dicoR = json.loads(response.text)

        print(dicoR)
    else:

        print("error")
        print(response.text)



def pretty_print_POST(req):
    """
    Une fonction d'affichage pour faciliter le debuggage
    et la construction de requete
    avant de tenter de l'envoyer réellement au serveur.

    Ce code est issu de stackoverflow :
    https://stackoverflow.com/questions/20658572/python-requests-print-entire-http-request-raw

    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    Parameters
    ----------
    req : STR
        la requete à afficher

    Exemple:
        url = "https//hello.com"
        APIheaders = {"X-API-KEY":myConst.API_KEY}

        req = requests.Request("POST",url, headers=APIheaders)
        prepared = req.prepare()
        pretty_print_POST(prepared)

    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
