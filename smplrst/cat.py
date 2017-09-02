import json

import os

import requests

import falcon

from xml.etree import ElementTree as ET

from pymongo import MongoClient

class CatEndpoint(object):

    def on_get(self, req, resp):
        #initialize connection, DB, and collection
        mongo_client = MongoClient(os.environ['MONGODB_HOST'], 27017)
        db = mongo_client.catdb
        collection = db.catimages

        #initialize dicts to hold BSON 'docs' for mongo
        cat_img_resp = {}
        img_doc = {}

        #build and make cat API call
        api_params = {
                      'api_key': os.environ['API_KEY'],
                      'format': 'xml'
                     }

        cat_api_req = requests.get('http://thecatapi.com/api/images/get', params=api_params)

        #grab needed bits from XML and put into dict for later easy JSON/BSON handling
        cat_resp_xml = ET.fromstring(cat_api_req.content)

        for elem in cat_resp_xml.iter():
            if elem.tag == 'url':
                img_doc['url'] = elem.text
            elif elem.tag == 'id':
                img_doc['id'] = elem.text
            elif elem.tag == 'source_url':
                img_doc['source_url'] = elem.text

        #build our JSON response
        cat_img_resp['image'] = img_doc

        resp.body = json.dumps(cat_img_resp, ensure_ascii=False)

        #put JSON 'doc' into our db collection
        collection.insert_one(cat_img_resp)
