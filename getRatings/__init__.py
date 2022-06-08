import logging
import json

import azure.functions as func

def main(req: func.HttpRequest, doc: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')

    if not doc:
        return func.HttpResponse('ratings not found', status_code=404)
    else:
        ratings = []
        for d in doc:
            payload_response = {
                "id": d['id'],
                "userId": d['userId'],
                "productId": d['productId'],
                "timestamp": d['timestamp'],
                "locationName": d['locationName'],
                "rating": d['rating'],
                "userNotes": d['userNotes']
            }
            ratings.append(payload_response)
        return func.HttpResponse(json.dumps(ratings), status_code=200)
