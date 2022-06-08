import json
import logging
import requests
import uuid

import azure.functions as func

def main(req: func.HttpRequest,  doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user = None
    product = None
    try:
        req_body = req.get_json()
        user_id = req_body.get('userId')
        product_id = req_body.get('productId')

        validator = {
            "not found": []
        }

        if not user_id:
            validator["not found"].append({'param': 'user_id'})
        else:
            user = find_user(user_id).json()['userId']
            if not user:
                validator["not found"].append({'user does not exist'})

        if not product_id:
            validator["not found"].append({'param': 'product_id'})
        else:
            product = find_user(product_id).json()['productId']
            if not user:
                validator["not found"].append({'product does not exist'})
        
    except ValueError:
        pass

    payload_response = {
        "id": str(uuid.uuid4()),
        "userId": user,
        "productId": product,
        "timestamp": "2018-05-21 21:27:47Z",
        "locationName": "teste felipe",
        "rating": 5,
        "userNotes": "I love the subtle notes of orange in this ice cream!"
    }

    if user_id and product_id:

        doc.set(func.Document.from_json(json.dumps(payload_response)))
        return func.HttpResponse(json.dumps(payload_response), status_code=200)
    else:
        return func.HttpResponse(
             json.dumps(validator),
             status_code=400
        )

def find_user(user_id):
    return requests.get(f'https://serverlessohapi.azurewebsites.net/api/GetUser?userId={user_id}')

def find_product(product_id):
    return requests.get(f'https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={product_id}')

