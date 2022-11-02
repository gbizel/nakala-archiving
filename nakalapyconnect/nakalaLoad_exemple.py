# -*- coding: utf-8 -*-
"""
@author: Sylvain Machefert 
"""
from string import Template

import pyexcel as pe
import re
import sys, os
import zipfile
import requests
import nklPushCorpus as npc

NAKALA_EMAIL = os.getenv('NAKALA_EMAIL', default=None)
NAKALA_KEY =  os.getenv('NAKALA_KEY', default=None)


if not NAKALA_KEY or not NAKALA_EMAIL:
	print "Missing bashrc variables : NAKALA_KEY / NAKALA_EMAIL"
	sys.exit()

source_filename = "file.ods"
sheet = pe.get_sheet(file_name=source_filename)

s = Template('<nkl:Data xmlns:dcterms="http://purl.org/dc/terms/" xmlns:nkl="http://nakala.fr/schema#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dcterms:title>$title</dcterms:title><dcterms:creator>$creator</dcterms:creator><dcterms:type>http://purl.org/dc/dcmitype/Sound</dcterms:type><dcterms:created>$date</dcterms:created><dcterms:identifier>$identifier</dcterms:identifier><nkl:inCollection></nkl:inCollection><nkl:accessEmail>user@domaine.fr</nkl:accessEmail><nkl:dataFormat>MPEG</nkl:dataFormat></nkl:Data>')

counter = 0
for row in sheet.rows():
	if row[0] == "CODE FICHIER":
		print "Header"
	else:
		record = {}
		record["title"] = row[12]
		record["creator_givenname"] = row[6]
		record["creator_surname"] = row[7]
		record["date"] = row[13]
		record["filename"] = row[0]

		record["filepath"] = "/media/usb/%s/%s" % (row[1], row[0])
		record["identifier"] = os.path.splitext(record["filename"])[0]

		if os.path.isfile(record["filepath"]):
			listFiles = [record["filepath"]]

			dicoMetas = {}
			dicoMetas["collectionsIds"] = ["11280/XXXXXXXX"]

			dicoMetas["status"] = "published"
			dicoMetas["metas"] = []

			# Type de document - son
			metaType = {"value": "http://purl.org/coar/resource_type/c_18cc",
			            "lang": "fr",
			            "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
			            "propertyUri": "http://nakala.fr/terms#type"
			            }
			dicoMetas["metas"].append(metaType)

			# Titre du document
			metaTitle={"value": record["title"],
			  "lang": "fr",
			  "typeUri": "http://www.w3.org/2001/XMLSchema#string",
			  "propertyUri": "http://nakala.fr/terms#title"
			  }
			dicoMetas["metas"].append(metaTitle)

			metaAuthor = {"value": {
			    "givenname": record["creator_givenname"],
			    "surname": record["creator_surname"],
			    "orcid":None
			     },
			  "propertyUri": "http://nakala.fr/terms#creator"
			  }
			dicoMetas["metas"].append(metaAuthor)

			metaCreated={"value": record["date"],
			  "typeUri": "http://www.w3.org/2001/XMLSchema#string",
			  "propertyUri": "http://nakala.fr/terms#created"
			}
			dicoMetas["metas"].append(metaCreated)

			metaLicense={"value": "InC",
			             "typeUri": "http://www.w3.org/2001/XMLSchema#string",
			             "propertyUri": "http://nakala.fr/terms#license"
			             }
			dicoMetas["metas"].append(metaLicense)

			doi = npc.post_datas(dicoMetas, listFiles)
			print "DOI ok : %s" % doi

			# On va ajouter les droits
			npc.give_rights(doi, "XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXX")

			row[-1] = doi
			sheet.row[counter] = row
			sheet.save_as(source_filename)
			print "Upload OK : %s" % doi
		else:
			print "%s/%s absent du DD" % (row[1], record["identifier"])
	counter = counter+1