import json

import falcon

from pymongo import MongoClient

class HistoryEndpoint(object):

    def on_get(self, req, resp):
        #initialize connection, DB, and collection
        mongo_client = MongoClient('localhost', 27017)
        db = mongo_client.catdb
        collection = db.catimages

        #initialize response data structs
        history_resp = {}
        doc_list = []

        for img in collection.find():
            doc_list.append(img['image'])

        history_resp['images'] = doc_list

        resp.body = json.dumps(history_resp, ensure_ascii=False)
