import json

import requests

import falcon

from xml.etree import ElementTree as ET

from pymongo import MongoClient

class CatEndpoint(object):

    def on_get(self, req, resp):
        #initialize connection, DB, and collection
        mongo_client = MongoClient('localhost', 27017)
        db = mongo_client.catdb
        collection = db.catimages

        #initialize dicts to hold BSON 'docs' for mongo
        cat_img_resp = {}
        img_doc = {}

        #call cat api, extract and convert needed bits into dict
        cat_api_req = requests.get('http://thecatapi.com/api/images/get?format=xml')

        cat_resp_xml = ET.fromstring(cat_api_req.content)

        for elem in cat_resp_xml.iter():
            if elem.tag == 'url':
                img_doc['url'] = elem.text
            elif elem.tag == 'id':
                img_doc['id'] = elem.text
            elif elem.tag == 'source_url':
                img_doc['source_url'] = elem.text

        #build our json response
        cat_img_resp['image'] = img_doc

        resp.body = json.dumps(cat_img_resp, ensure_ascii=False)

        #put json 'doc' into our db collection
        collection.insert_one(cat_img_resp)
