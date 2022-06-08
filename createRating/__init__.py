import json
import logging
import requests

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        user_id = req_body.get('userId')
        product_id = req_body.get('productId')

        validator = {
            "not found": []
        }

        if not user_id or not find_user:
            validator["not found"].append({'param': 'user_id'})
        
        if not product_id or not find_product:
            validator["not found"].append({'param': 'product_id'}) 

    except ValueError:
        pass

    if user_id and product_id:
        return func.HttpResponse('user and product found', status_code=200)
    else:
        return func.HttpResponse(
             json.dumps(validator),
             status_code=400
        )

def find_user(user_id):
    response = requests.get(f'https://serverlessohapi.azurewebsites.net/api/GetUser?userId={user_id}')
    return response.status_code == 200

def find_product(product_id):
    response = requests.get(f'https://serverlessohapi.azurewebsites.net/api/GetProduct?productId={product_id}')
    return response.status_code == 200