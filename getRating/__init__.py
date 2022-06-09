import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, doc: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.params.get('id')

    if not doc:
        return func.HttpResponse('rating not found', status_code=404)
    else:
        payload_response = {
            "id": doc[0]['id'],
            "userId": doc[0]['userId'],
            "productId": doc[0]['productId'],
            "timestamp": doc[0]['timestamp'],
            "locationName": doc[0]['locationName'],
            "rating": doc[0]['rating'],
            "userNotes": doc[0]['userNotes']
        }
        return func.HttpResponse(json.dumps(payload_response, indent=True), status_code=200)