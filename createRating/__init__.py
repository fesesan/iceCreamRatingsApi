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
    except ValueError:
        pass
    else:
        name = req_body.get('name')

    if user_id and product_id:
        return func.HttpResponse(f"Hello, {user_id} and {product_id}. This HTTP triggered function executed successfully.")
    else:
        response = requests.get('https://serverlessohapi.azurewebsites.net/api/GetProducts').json()
        logging.info(response)
        return func.HttpResponse(
             'teste ok',
             status_code=200
        )






def validate_user(user_id):
    pass

def validate_product(product_id):
    pass