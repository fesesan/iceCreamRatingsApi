import json
import logging
import requests
import uuid
from  datetime import datetime
import azure.functions as func

def main(req: func.HttpRequest,  doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user = None
    product = None
    rating = None
    locationName = None
    userNotes = None

    try:
        req_body = req.get_json()
        user_id = req_body.get('userId')
        product_id = req_body.get('productId')
        rating = req_body.get('rating')
        locationName = req_body.get('locationName')
        userNotes = req_body.get('userNotes')

        validator = {
            "errors": []
        }

        if not user_id:
            validator["errors"].append({'param': 'user_id'})
        else:
            response = find_user(user_id)
            if response.status_code == 400:
                validator["errors"].append({'message':'user does not exist'})
            else:
                user = response.json()['userId']

        if not product_id:
            validator["errors"].append({'param': 'product_id'})
        else:
            response = find_product(product_id)
            if response.status_code == 400:
                validator["errors"].append({'message': 'product does not exist'})
            else:
                product = response.json()['productId']
        
        if not rating:
            validator["errors"].append({'param': 'rating'})
        else:
            if not validate_rating_range(rating):
                print('nao validou')
                validator["errors"].append({'message': 'rating 0 to 5'})        

    except ValueError:
        print('erro ao converter')

    if not validator['errors']:
        payload_response = {
            "id": str(uuid.uuid4()),
            "userId": user,
            "productId": product,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'),
            "locationName": locationName,
            "rating": str(rating),
            "userNotes": userNotes
        }
        doc.set(func.Document.from_json(json.dumps(payload_response)))
        return func.HttpResponse(json.dumps(payload_response, indent=True), status_code=200)
    else:
        print(validator)
        return func.HttpResponse(
             json.dumps(validator),
             status_code=400
        )

def validate_rating_range(rating):
    return rating in [0,1,2,3,4,5]


def find_user(user_id):
    return requests.get(f'https://serverlessohapi.azurewebsites.net/api/GetUser?userId={user_id}')

def find_product(product_id):
    return requests.get(f'https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={product_id}')

