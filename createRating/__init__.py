import json
import logging
import requests

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        response = requests.get('https://serverlessohapi.azurewebsites.net/api/GetProducts').json()
        logging.info(response)
        return func.HttpResponse(
             'teste ok',
             status_code=200
        )