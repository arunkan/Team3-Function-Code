import logging
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import json

import azure.functions as func


def main(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            data = req.get_json()
        except ValueError:
            pass

    if len(data['summary_tables']) > 0:
            for j in range(0, len(data['summary_tables'])):
                if data['summary_tables'][j]['table']['formatted'] != None:
                    temp = data['summary_tables'][j]['table']['formatted']

                    html = temp.replace('\n', ' ')
                    html = html.replace('\r', '')

                    soup = BeautifulSoup(html, features="html.parser")
                    data['summary_tables'][j]['table']['formatted'] = soup.get_text()

    for time in ['approved_at', 'created_at', 'read_at']:
        if data[time] is not None:
            s = datetime.utcfromtimestamp(data[time])
            data[time] = s.strftime("%Y-%m-%dT%H:%M:%S.%fZ") # Prints "2020-01-03T05:30:44.201000Z"


    outputblob.set(json.dumps(data))

    return func.HttpResponse(
         str(data['created_at']),
         status_code=200
    )
